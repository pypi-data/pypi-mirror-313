import polars as pl
import pandas as pd
from colorama import Fore
from openpyxl.utils.cell import column_index_from_string, coordinate_from_string, get_column_letter
from core_pro.config import GoogleAuthentication
from rich import print


class Sheet(GoogleAuthentication):
    service_type = 'sheets'

    def __init__(self, spreadsheet_id):
        super().__init__(Sheet.service_type)
        self.spreadsheet_id = spreadsheet_id
        self.status = '[green3]🐶 Sheet[/green3]'

    def get_list_sheets(self) -> list:
        spreadsheet = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
        list_sheets = [i['properties']['title'] for i in spreadsheet['sheets']]
        print(f'{self.status} There are {len(list_sheets)} sheets')
        print(list_sheets)
        return list_sheets

    def google_sheet_into_df(
            self,
            sheet_name: str,
            sheet_range: str,
            value_render_option: str = 'FORMATTED_VALUE',
            use_polars: bool = True,
    ) -> pl.DataFrame | pd.DataFrame:
        """
        Read google sheet and return a DataFrame
        :param use_polars: True, False
        :param value_render_option: default FORMATTED_VALUE, UNFORMATTED_VALUE, FORMULA
        :param sheet_name: google sheet name
        :param sheet_range: google sheet range
        :return: a DataFrame
        """
        # load
        range_update = f'{sheet_name}!{sheet_range}'
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=range_update,
            valueRenderOption=value_render_option,
        ).execute()

        # to df
        print(f"{self.status} Loaded at {range_update}")
        if use_polars:
            max_length = max(len(v) for v in result['values'])
            padded_data = [v + [None] * (max_length - len(v)) for v in result['values'][1:]]
            return pl.DataFrame(padded_data, schema=result['values'][0], orient='row')
        else:
            return pd.DataFrame(result['values'][1:], columns=result['values'][0])

    def create_new_sheet(self, sheet_title):
        # Check if exists:
        lst_sheets_exist = self.get_list_sheets()
        if sheet_title in lst_sheets_exist:
            sheet_title = f'{sheet_title}_copy'

        # Create the request body
        request_body = {
            'requests': [{
                'addSheet': {
                    'properties': {'title': sheet_title}
                }
            }]
        }

        # Execute the request
        response = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id,body=request_body).execute()
        new_sheet_id = response['replies'][0]['addSheet']['properties']['sheetId']
        print(f"{self.status} Create New Sheet: {sheet_title}")
        return new_sheet_id

    def clear_gsheet(self, sheet_name: str, sheet_range: str):
        """
        Clear google sheet
        :param sheet_name: sheet name
        :param sheet_range: ex: "A:C"
        :return: None
        """
        # clear
        name = f'{sheet_name}!{sheet_range}'
        self.service.spreadsheets().values().clear(spreadsheetId=self.spreadsheet_id, range=name, body={}).execute()

    def update_value_single_axis(
            self,
            value_input: str | list,
            sheet_name: str,
            sheet_range: str,
            COLUMNS_or_ROWS: str = 'ROWS',
            value_option: str = 'RAW'
    ):
        """
        Update google sheet value
        :param sheet_range: range update ex: 'A1'
        :param value_input: value need to update: [2, 3, 4] or [[2, 3, 4], [2, 3, 4]] if multi==True
        :param sheet_name: sheet name
        :param COLUMNS_or_ROWS: default by ROWS
        :param value_option: default = 'RAW', or 'USER_ENTERED' or INPUT_VALUE_OPTION_UNSPECIFIED
        :return: result
        """

        range_update = f"{sheet_name}!{sheet_range}"
        if isinstance(value_input, list):
            values = value_input
        else:
            values = [[value_input]]
        body = {
            'values': values,
            'majorDimension': COLUMNS_or_ROWS
        }
        self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=range_update,
            valueInputOption=value_option,
            body=body
        ).execute()
        print(f"{self.status} Update values at: {range_update}")

    def make_a_copy_sheet(self, sheet_id: str, dup_sheet_name: str):
        """
        Para:
        - spreadsheet_id: template_sheet
        - sheet_id: template_worksheet
        - dup_sheet_name: sheet to copy
        """
        # copy
        duplicated_spreadsheet_body = {'destination_spreadsheet_id': dup_sheet_name}
        request = self.service.spreadsheets().sheets().copyTo(
            spreadsheetId=self.spreadsheet_id,
            sheetId=sheet_id,
            body=duplicated_spreadsheet_body
        )
        response = request.execute()
        return response

    def rename_worksheet(self, sheet_id: str, new_title: str):
        requests = {
            "updateSheetProperties": {
                "properties": {
                    "sheetId": sheet_id,
                    "title": new_title,
                },
                "fields": "title",
            }
        }
        body = {
            'requests': requests
        }
        self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id, body=body).execute()

    def delete_worksheet(self, sheet_id: str):
        body = {
            'requests': {
                'deleteSheet': {"sheetId": sheet_id}
            }
        }
        self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id, body=body).execute()

    def get_worksheet_properties(self, sheet_name: str):
        spreadsheet = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
        lst_worksheet = list(filter(lambda x: x.get('properties').get('title') == sheet_name, spreadsheet['sheets']))
        if lst_worksheet:
            return lst_worksheet[0].get('properties')


class SheetFormat(GoogleAuthentication):
    service_type = 'sheets'

    def __init__(self, spreadsheet_id):
        super().__init__(Sheet.service_type)
        self.spreadsheet_id = spreadsheet_id
        self.status = f'{Fore.LIGHTGREEN_EX}🐶 Format Sheet:{Fore.RESET}'

    def _range(self, ws_id: str, position: str, num_col: int = None):
        pos_col, pos_row = coordinate_from_string(position)
        pos_col = column_index_from_string(pos_col)

        self.my_range = {
            'sheetId': ws_id,
            'startRowIndex': pos_row - 1,
            'endRowIndex': pos_row,
            'startColumnIndex': pos_col - 1,
            'endColumnIndex': pos_col,
        }
        if num_col:
            self.my_range['endColumnIndex'] = pos_col + num_col - 1

    def title(self, ws_id: str, position: str):
        color_orange = hex_to_rgb('#ff6d01', 'sheets')
        self._range(ws_id, position)
        request = [{
            'repeatCell': {
                'range': self.my_range,
                'cell': {
                    'userEnteredFormat': {
                        'textFormat': {
                            'foregroundColor': color_orange,
                            'bold': True,
                            'fontSize': 12,
                            'fontFamily': 'Roboto'
                        }
                    }
                },
                'fields': 'userEnteredFormat(textFormat)'
            }
        }]
        body = {"requests": request}
        self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id, body=body).execute()
        print(f'{self.status} Highlight title at {position}:{get_column_letter(self.my_range['endColumnIndex'])}')

    def header(self, ws_id: str, position: str, num_col: int):
        color_grey = hex_to_rgb('#b7b7b7', 'sheets')
        self._range(ws_id, position, num_col)
        request = [
            {
                'repeatCell': {
                    'range': self.my_range,
                    'cell': {
                        'userEnteredFormat': {
                            'backgroundColor': color_grey,
                            'horizontalAlignment': 'CENTER',
                            'textFormat': {
                                'bold': False,
                                'fontFamily': 'Roboto'
                            }
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
                }
            },
        ]
        body = {"requests": request}
        self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id, body=body).execute()
        print(f'{self.status} Highlight header at {position}')

    def frozen_view(self, ws_id: str, frozen_rows: int = 2):
        request = [{
            'updateSheetProperties': {
                'properties': {
                    'sheetId': ws_id,
                    'gridProperties': {'frozenRowCount': frozen_rows}
                },
                'fields': 'gridProperties.frozenRowCount'
            }
        }]
        body = {"requests": request}
        self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id, body=body).execute()
        print(f'{self.status} Frozen views up to {frozen_rows} rows')

    def percentage_number(self,  ws_id: str, cell_range: str):
        requests = [{
            "repeatCell": {
                "range": {
                    "sheetId": ws_id,
                    "startRowIndex": 0,
                    "endRowIndex": len(cell_range.split(':')[1].strip('0123456789')) + 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": len(cell_range.split(':')[1].strip('0123456789')) + 1
                },
                "cell": {
                    "userEnteredFormat": {
                        "numberFormat": {
                            "type": "PERCENT",
                            "pattern": "0.00%"
                        }
                    }
                },
                "fields": "userEnteredFormat.numberFormat"
            }
        }]
        # Execute the request
        body = {'requests': requests}
        self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id, body=body).execute()
        print(f"Cells {cell_range} formatted as percentage.")


def hex_to_rgb(hex_code, mode='sheets'):
    hex_code = hex_code.lstrip('#')
    rgb = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
    if mode == 'sheets':
        return {i: v / 255 for i, v in zip(['red', 'green', 'blue'], rgb)}
    else:
        return rgb
