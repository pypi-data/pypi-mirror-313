class OperatorTicketReport:
    """Operator Ticket Report"""

    def __init__(self, db, company_id: str, vendor_deficiency_results: dict) -> None:
        self.db = db
        self.company_id = company_id
        self.vendor_deficiency_results = vendor_deficiency_results

    def filter_operators(self) -> list:
        """Filter Operators"""
        operators = [x for x in self.vendor_deficiency_results['rows']
                     if x['Subscription Type'] == 0]

        distinct_operators = []
        for operator in operators:
            distinct_operators.append({
                'vendor_id': operator['vendor_id'],
                'Vendor Name': operator['Vendor Name'],
                'Subscription Type': operator['Subscription Type'],
                'Vendor Tags': operator['Vendor Tags'],
                'Vendor Rating': operator['Vendor Rating'],
                'Admin Name': operator['Admin Name'],
                'Admin Email': operator['Admin Email'],
                'Admin Phone': operator['Admin Phone'],
                'Vendor Deficiencies': '\n'.join([x['Current Deficiencies'] for x in self.vendor_deficiency_results['rows'] if x['vendor_id'] == operator['vendor_id']])
            })

        return [dict(t) for t in {tuple(d.items()) for d in distinct_operators}]

    def prime(self, tickets: list) -> list:
        """Prime"""
        doc_questions = self.db.get_results(
            query=f"SELECT * FROM c WHERE c.type = 'docQuestion' AND ARRAY_CONTAINS({list(set([x['docId'] for x in tickets]))}, c.docId)")

        ticket_headers = []
        for ticket in tickets:
            for question in doc_questions:
                if ticket['docId'] == question['docId']:

                    item = {
                        "header": f"{ticket['docType']}: {question['text']}",
                        "key": question['key'],
                        # "ticket_id": ticket['id']
                    }
                    if item not in ticket_headers:
                        ticket_headers.append(item)
        print(f'PRIME: {ticket_headers}')
        return ticket_headers

    def get_ocr_output(self, header_list: list, ticket: dict) -> dict:
        """Get OCR Output"""
        for item in ticket['ocrOutput']['values']:
            for key in header_list:
                if item['key'] == key['key']:

                    return {
                        'key': [x['header'] for x in header_list if x['header'].split(':')[0] == ticket['docType']][0],
                        'val': item['updatedValue'] if item['updatedValue'] != '' else item['ocrValue'],
                        'vendor_id': ticket['vendorId']
                    }

    def build_final(self, tickets: list, header_list: list):
        """Build final"""
        results = []
        for inner in tickets:

            for k, v in inner.items():
                if k == 'ocrOutput':
                    ocr_value = self.get_ocr_output(header_list, inner)
                    results.append(ocr_value)

        return results

    def build_operator_tickets_report(self) -> dict:
        """Build Operator Tickets Report"""
        operators = self.filter_operators()

        tickets = self.db.get_results(
            query=f"SELECT * FROM c WHERE c.type = 'vendorDoc' AND c.docClass = 'additionalRequirement' AND c.status != 'Not Submitted' AND c.employerId = '{self.company_id}' AND ARRAY_CONTAINS({[x['vendor_id'] for x in operators]}, c.vendorId)")

        ticket_headers = self.prime(tickets)
        ticket_results = self.build_final(tickets, ticket_headers)

        rows = []

        for operator in operators:
            rows.append({
                'vendor_id': operator['vendor_id'],
                'Vendor Name': operator['Vendor Name'],
                'Subscription Type': operator['Subscription Type'],
                'Vendor Tags': operator['Vendor Tags'],
                'Vendor Rating': operator['Vendor Rating'],
                'Admin Name': operator['Admin Name'],
                'Admin Email': operator['Admin Email'],
                'Admin Phone': operator['Admin Phone'],
                'Vendor Deficiencies': operator['Vendor Deficiencies']
            })

        final_headers = list(rows[0].keys()) + [x['header']
                                                for x in ticket_headers]
        final_rows = []
        for item in rows:
            final_rows.append(
                {**item, **{x['header']: '' for x in ticket_headers}})

        print(ticket_results)
        for item in final_rows:
            for ticket in ticket_results:
                if item['vendor_id'] == ticket['vendor_id']:
                    item[ticket['key']] = ticket['val']

        more_final_rows = []
        for item in final_rows:
            item.pop('vendor_id')
            more_final_rows.append(item)

        final_headers.remove('vendor_id')

        return {
            'file_name': 'Operator_Ticket_Report.csv',
            'headers': final_headers,
            'rows': more_final_rows
        }
