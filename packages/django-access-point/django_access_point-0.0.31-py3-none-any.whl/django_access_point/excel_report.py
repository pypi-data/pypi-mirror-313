import openpyxl
from django.http import HttpResponse
from django.core.paginator import Paginator


class ExcelReportGenerator:
    """
    A base class to generate downloadable Excel reports from any given queryset.
    """

    def __init__(self, title, queryset, get_headers, get_row_data, chunk_size=100):
        self.title = title
        self.queryset = queryset
        self.chunk_size = chunk_size
        self.get_headers = get_headers
        self.get_row_data = get_row_data

    def generate_report(self):
        """
        Generate the Excel report and return it as an HTTP response.
        """
        # Create a workbook and a sheet
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = self.title

        # Define headers based on model fields and custom fields
        headers = self.get_headers()

        # Write headers to the first row
        ws.append(headers)

        # Write data rows from the queryset
        self.write_data(ws)

        # Set the HTTP response for downloading the Excel file
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = "attachment; filename=report.xlsx"

        # Save the workbook to the response object
        wb.save(response)

        return response

    def write_data(self, ws):
        """
        Write data to the Excel sheet in chunks to avoid memory overload.
        """
        paginator = Paginator(self.queryset, self.chunk_size)

        for page_number in paginator.page_range:
            page = paginator.page(page_number)

            for obj in page.object_list:
                row = self.get_row_data(obj)
                ws.append(row)
