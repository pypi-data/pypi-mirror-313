from pathlib import Path
import pandas as pd
import polars as pl
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import trino
import os
from rich import print
from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
    SpinnerColumn
)
from rich.console import Group
from rich.panel import Panel
from rich.live import Live


class DataPipeLine:
    def __init__(
            self,
            query: str,
            count_rows: bool = False,
            use_polars: bool = True,
    ):
        self.query = f"SELECT COUNT(*) FROM ({query})" if count_rows else query
        self.use_polars = use_polars or count_rows
        self.count_rows = count_rows
        self.df = None
        self.status = '[bright_blue]🤖 JDBC[/bright_blue]'

    def debug_query(self):
        print(self.query)

    def _records_to_df(self, records, columns: list):
        if self.use_polars:
            self.df = pl.DataFrame(records, orient='row', schema=columns)
        else:
            self.df = pd.DataFrame(records, columns=columns)

        # message
        message = (
            f"Total rows: {self.df.to_numpy()[0][0]:,.0f}" if self.count_rows
            else f"Data shape ({self.df.shape[0]:,.0f}, {self.df.shape[1]})"
        )
        return message

    def export_df(self, save_path: Path, file_name: str):
        save_path.parent.mkdir(parents=True, exist_ok=True)
        if self.count_rows:
            self.df = self.df.rename({'_col0': file_name})
            self.df.write_ndjson(save_path.parent / f'log_count_{file_name}.json')
        elif self.use_polars:
            self.df.write_parquet(save_path)
        else:
            self.df.to_parquet(save_path, index=False, compression='zstd')

    def _connection(self):
        username, password = os.environ['PRESTO_USER'], os.environ['PRESTO_PASSWORD']
        conn = trino.dbapi.connect(
            host='presto-secure.data-infra.shopee.io',
            port=443,
            user=username,
            catalog='hive',
            http_scheme='https',
            source=f'(50)-(vnbi-dev)-({username})-(jdbc)-({username})-(SG)',
            auth=trino.auth.BasicAuthentication(username, password)
        )
        return conn

    def _progress(self):
        overall = Progress(
            TimeElapsedColumn(),
            TextColumn("•"),
            TextColumn("{task.description}"),
        )

        query_progress = Progress(
            TextColumn("{task.description}"),
            SpinnerColumn("simpleDots"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            BarColumn(),
            transient=True
        )

        fetch_progress = Progress(
            TextColumn("{task.description}"),
            SpinnerColumn("simpleDots"),
            transient=True
        )

        progress_group = Group(Panel(Group(overall, query_progress, fetch_progress)))
        return progress_group, overall, query_progress, fetch_progress

    def run_presto_to_df(
            self,
            save_path: Path = None,
            file_name: str = '',
    ):
        # connection
        conn = self._connection()
        cur = conn.cursor()

        # verbose
        progress_group, overall, query_progress, fetch_progress = self._progress()
        thread = ThreadPoolExecutor(1)

        # run
        async_result = thread.submit(cur.execute, self.query)
        with Live(progress_group):
            task_id_overall = overall.add_task(f"{self.status} Query file name [{file_name}], Count rows: [{self.count_rows}]")
            task_id_query = query_progress.add_task("[cyan]Presto to Local", total=100)
            # query
            while not async_result.done():
                memory = cur.stats.get('peakMemoryBytes', 0) * 10 ** -9
                perc = 0
                stt = cur.stats.get('state', 'Not Ready')
                if stt == "RUNNING":
                    perc = round((cur.stats.get('completedSplits', 1e-3) * 100.0) / (cur.stats.get('totalSplits', 0)), 2)
                status = f"{stt} - Memory {memory:,.0f}GB"
                query_progress.update(task_id_query, description=status, advance=perc)
                sleep(5)

            task_id_fetch = fetch_progress.add_task("Fetching")
            records = cur.fetchall()

            # result
            columns = [i[0] for i in cur.description]
            text = self._records_to_df(records, columns)
            if save_path:
                self.export_df(save_path, file_name)

            # update status
            message = f"{self.status} [bold green]Done:[/] {text}"
            overall.update(task_id_overall, description=message)
            query_progress.update(task_id_query, visible=False)
            fetch_progress.update(task_id_fetch, visible=False)
        return self.df


# query = f"""
#     select
#         item_id
#     from
#         mp_order.dwd_order_item_all_ent_df__vn_s0_live o
#     limit 100
# """
# DataPipeLine(query).run_presto_to_df()
