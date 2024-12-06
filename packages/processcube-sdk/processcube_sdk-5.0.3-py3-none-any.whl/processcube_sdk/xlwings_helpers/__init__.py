import pandas as pd

def make_link(link, title):
    return f'=HYPERLINK("{link}"; "{title}")'

def make_email(email, title):
    return f'=HYPERLINK("mailto:{email}"; "{title}")'

def sheet_by_name(book, sheet_name, create=True):
    if sheet_name in [sheet.name for sheet in book.sheets]:
        sheet = book.sheets[sheet_name]
    else:
        if create:
            sheet = book.sheets.add(sheet_name)
        else:
            sheet = None

    return sheet

def get_config(book):
    sheet = sheet_by_name(book, 'Report_Config', create=False)
    
    if sheet is None:
        sheet = sheet_by_name(book, 'Config', create=False)

    if sheet is None:
        raise Exception('Config-Sheet not found')

    config = {}

    data = sheet.range("A1").expand().value

    if type(data) is not list:
        data = [data]

    for entry in data:
        key, value = entry[0], entry[1]

        config[str(key).lower()] = str(value)

    return config

def default_table_formatter(rng, df: pd.DataFrame):
    row_odd_color = "#f3f3f3"
    row_even_color = "#FFFFFF"
    header_color = "#bdbdbd"

    # Header
    rng[0, :].color = header_color

    # Rows
    for ix, row in enumerate(rng.rows[1:]):
        if ix % 2 == 0:
            row.color = row_odd_color  # Even rows
        else:
            row.color = row_even_color
            #row.font.bold = True

    # Columns
    #for ix, col in enumerate(df.columns):
    #    if "two" in col:
    #        rng[1:, ix].number_format = "0.0%"

def fill_sheet(book, sheet_name: str, df: pd.DataFrame, formatter_options: dict = {}, cell_options: dict = {'index': False}):
    report_sheet = sheet_by_name(book, sheet_name)
    
    if formatter_options:
        cell_options['formatter'] = formatter_options

    report_cell = report_sheet["A1"]
    report_cell.expand().clear_contents()
    
    report_cell.options(**cell_options).value = df

    report_cell.offset(row_offset=1).columns.autofit()

def fill_sheet_and_result_json(book, sheet_name: str, df: pd.DataFrame, formatter_options: dict = {}, cell_options: dict = {'index': False}):
    fill_sheet(book, sheet_name, df, formatter_options, cell_options)
    
    book_json = book.json()
    
    return book_json

def fill_report_sheet_and_result_json(book, df: pd.DataFrame, formatter_options: dict = {}, cell_options: dict = {'index': False}):
    book_config = get_config(book)

    return fill_sheet_and_result_json(book, book_config['sheet'], df, formatter_options, cell_options)
    
def default_book_json(config_values: dict = {}):
    data = {'book': {
                'active_sheet_index': 1,
                'name': 'Reporting [local Dev] (Arbeitsleistung v2)',
                'selection': 'A1'
            },
            'client': 'Google Apps Script',
            'names': [],
            'sheets': [{'name': 'Config',
             'pictures': [],
             'values': [['Report', 'arbeitsleistung_v2'],
                        ['Sheet', 'Arbeitsleistung'],
                        ['Start', '2023-02-01T00:00:00.000Z'],
                        ['Ende', '2023-02-28T00:00:00.000Z']]},
            {'name': 'Arbeitsleistung', 'pictures': [], 'values': [[]]},
            {'name': 'Summen zur Arbeitsleistung',
             'pictures': [],
             'values': [[]]},
            {'name': 'Arbeitsleistung v2', 'pictures': [], 'values': [[]]}], 'version': '0.28.7'}
    
    if config_values != {}:
        index = [sheet['name'] for sheet in data['sheets']].index('Config')
        data['sheets'][index]['values'].extend([[key, value] for key, value in config_values.items()])

    return data
