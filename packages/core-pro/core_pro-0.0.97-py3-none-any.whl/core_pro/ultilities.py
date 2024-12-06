from .GSheet import Sheet, SheetFormat
import polars as pl
from pathlib import Path
import requests
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from time import sleep, perf_counter
from tqdm import tqdm
from datetime import timedelta, datetime
from openpyxl.utils.cell import get_column_letter, column_index_from_string, coordinate_from_string
from itertools import batched
import socket
from datetime import date
from rich import print


def update_df(df, sheet_name: str, spreadsheet_id: str, start: str = 'A1'):
    # Call sheet
    sheet = Sheet(spreadsheet_id)
    # Dataframe type
    if not isinstance(df, pl.DataFrame):
        df = pl.DataFrame(df)
    values = [df.columns]
    values.extend(df.with_columns(pl.all().cast(pl.String)).to_numpy().tolist())
    # Check existed sheets
    lst_sheets = sheet.get_list_sheets()
    if sheet_name not in lst_sheets:
        sheet.create_new_sheet(sheet_name)
    # Export to sheets
    end = get_column_letter(len(values[0]) + column_index_from_string(coordinate_from_string(start)[0]) - 1)
    sheet.clear_gsheet(sheet_name, sheet_range=f"{start}:{end}")
    sheet.update_value_single_axis(
        sheet_range=f"{start}:{end}",
        value_input=values,
        sheet_name=sheet_name,
        value_option='USER_ENTERED'
    )


def format_df(
        sheet_name: str,
        spreadsheet_id: str,
        frozen_rows: int = None,
        position_title: str = None,
        position_df: str = None,
        num_col_format_df: int = None,
        format_pct: str = None
) -> None:
    """
    Format google sheet
    :param sheet_name: sheet_name
    :param spreadsheet_id: spreadsheet_id
    :param frozen_rows: 2
    :param position_title: 'A'
    :param position_df: 'A'
    :param num_col_format_df: 2
    :param format_pct: 'A1:B'
    """
    # Get sheet_id
    sheet = Sheet(spreadsheet_id)
    ws_id = sheet.get_worksheet_properties(sheet_name)['sheetId']
    # Format
    format_sheet = SheetFormat(spreadsheet_id)
    # Format: frozen
    if frozen_rows:
        format_sheet.frozen_view(ws_id, frozen_rows)
    # Format: Title
    if position_title:
        format_sheet.title(ws_id, position_title)
    # Header DF
    if not position_df:
        cor_col, cor_row = coordinate_from_string(position_title)
        cor_row += 1
        position_df = ''.join((cor_col, str(cor_row)))
    if position_df:
        format_sheet.header(ws_id, position_df, num_col_format_df)
    if format_pct:
        format_sheet.percentage_number(ws_id, format_pct)


def make_dir(folder_name: str | Path) -> None:
    """Make a directory if it doesn't exist"""
    if isinstance(folder_name, str):
        folder_name = Path(folder_name)
    if not folder_name.exists():
        folder_name.mkdir(parents=True, exist_ok=True)


def make_sync_folder(folder_name: str) -> Path:
    dict_ = {
        'kevinz3600': Path.home() / f'Downloads/Data/{folder_name}',
        'PL436MJK23': Path.home() / f'Downloads/Data/{folder_name}',
        'kevin-x670': Path(f'/media/kevin/data_4t/{folder_name}'),
    }
    ROOT_PATH = dict_[socket.gethostname()]
    make_dir(ROOT_PATH)
    return ROOT_PATH


def update_stt(stt: str, pos: int, sheet_id: str, sheet_name: str):
    Sheet(sheet_id).update_value_single_axis(sheet_range=f'I{pos}', sheet_name=sheet_name, value_input=stt)


def rm_old_file(path, days: int, file_type: str):
    check_date = datetime.today().date() - timedelta(days=days)
    print(f'Files {file_type} before {check_date} ({days} days) will be removed')

    for file in Path(path).glob(f'*.{file_type}'):
        mdate = datetime.fromtimestamp(file.stat().st_mtime).date()
        if mdate < check_date:
            print(f'Remove: file {file.name} - mdate: {mdate}')
            file.unlink()


def rm_all_folder(path: Path | str) -> None:
    """Remove all files in folder recursively"""
    if isinstance(path, str):
        path = Path(path)

    if path.exists():
        for child in path.glob('*'):
            if child.is_file():
                child.unlink()
            else:
                rm_all_folder(child)

        path.rmdir()


def sleep_with_progress(seconds: int, desc: str = ''):
    """ Sleep until specified number of seconds has elapsed"""
    with tqdm(total=seconds, desc=desc) as pbar:
        for _ in range(seconds):
            sleep(1)
            pbar.update(1)


def upload_to_datahub(file_path: Path, api_endpoint: str, ingestion_token: str, sleep_time: int = 10, max_retries: int = 3):
    """ Uploads csv file to DataHub"""

    def my_callback(monitor):
        pbar.update(monitor.bytes_read - pbar.n)

    # files
    file_name = str(file_path)
    file_parent_dir = str(file_path.parent)

    # monitor
    m = MultipartEncoder(fields={
        'file': (file_name, open(file_name, 'rb'), 'text/plain'),
        'parent_dir': file_parent_dir
    })
    me = MultipartEncoderMonitor(m, my_callback)
    headers = {'data-ingestion-token': ingestion_token, 'Content-Type': me.content_type}
    total_size = m.len

    # log config
    desc = 'Uploading to DataHub'
    for attempt in range(max_retries):
        # upload
        with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024, desc=desc, leave=True) as pbar:
            try:
                response = requests.request('POST', api_endpoint, headers=headers, data=me)
            except requests.exceptions.ConnectionError:
                sleep_with_progress(60 * sleep_time, desc='Waiting DataHub')
                break
        # log
        message = response.json().get('message')
        code = response.status_code
        if response.status_code == 200:
            return response
        else:
            sleep_with_progress(60 * sleep_time, desc='Waiting DataHub')

    if attempt == max_retries - 1:
        print('[DataHub] Max retries reached. Unable to upload.')


def time_decorator(func):
    def wrapper(*args, **kwargs):
        begin_time = perf_counter()
        output = func(*args, **kwargs)
        end_time = perf_counter() - begin_time
        print(f"[Execution Time] {func.__name__}: {end_time:,.2f} sec")
        return output

    return wrapper


def create_batch_index(total_rows: int, n_size: int) -> dict:
    batches = list(batched(range(0, total_rows), n_size))
    return {i: batches[i] for i in range(len(batches))}


def create_batches_by_month(start: date, end: date) -> list:
    lst = [i.date() for i in pl.datetime_range(start, end, "1mo", eager=True)]
    lst_2 = [i for i in lst[1:]]
    run = [(i, v - timedelta(days=1)) for i, v in zip(lst[:-1], lst_2)]
    print(run)
    return run
