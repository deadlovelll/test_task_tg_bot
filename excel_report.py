from openpyxl import Workbook

def create_xlsx_report(data):
    workbook = Workbook()
    
    for account, stats in data.items():
        sheet = workbook.create_sheet(title=f"Account {account}")
        sheet.append(["Название объявления", "Отвеченные звонки", "Звонки всего", "Новые звонки", "Новые и отвеченные"])

        for item in stats:
            sheet.append([
                item.get("item_name"),
                item.get("answered"),
                item.get("calls"),
                item.get("new"),
                item.get("newAnswered"),
            ])

    return workbook
