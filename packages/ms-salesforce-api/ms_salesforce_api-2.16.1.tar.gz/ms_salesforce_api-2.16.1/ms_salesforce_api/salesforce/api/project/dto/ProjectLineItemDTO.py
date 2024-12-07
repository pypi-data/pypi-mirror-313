from datetime import datetime


class ProjectLineItemDTO:
    def __init__(
        self,
        id,
        created_date,
        last_modified_date,
        product_name,
        starting_date,
        quantity,
        unit_price,
        total_price,
        ending_date,
        effort,
        ms_pli_name,
        country,
        project_code,
        project_id,
    ):
        self.id = id
        self.created_date = created_date
        self.last_modified_date = last_modified_date
        self.product_name = product_name
        self.starting_date = starting_date
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_price = total_price
        self.ending_date = ending_date
        self.effort = effort
        self.ms_pli_name = ms_pli_name
        self.country = country
        self.project_code = project_code
        self.project_id = project_id

    @classmethod
    def from_salesforce_record(cls, record, project_id):
        def _parse_created_date(created_date):
            try:
                dt = datetime.strptime(
                    created_date,
                    "%Y-%m-%dT%H:%M:%S.%f%z",
                )

                return dt.strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                return ""

        product_name = (
            record.get("ProductNew__r", {}).get("Name")
            if record.get("ProductNew__r")
            else None
        )
        return cls(
            id=record.get("Id"),
            created_date=_parse_created_date(record.get("CreatedDate")),
            last_modified_date=_parse_created_date(
                record.get("LastModifiedDate")
            ),
            product_name=product_name,
            starting_date=record.get("Starting_Date__c"),
            quantity=record.get("Quantity__c"),
            unit_price=record.get("UnitPrice__c"),
            total_price=record.get("Total_Price__c"),
            ending_date=record.get("Ending_Date__c"),
            effort=record.get("Effort__c"),
            ms_pli_name=record.get("MS_PLI_Name__c"),
            country=record.get("Country__c"),
            project_code=record.get("MS_Project_Code__c"),
            project_id=project_id,
        )

    def to_dict(self):
        return {
            "country": self.country,
            "created_date": self.created_date,
            "effort": self.effort,
            "ending_date": self.ending_date,
            "id": self.id,
            "last_modified_date": self.last_modified_date,
            "ms_pli_name": self.ms_pli_name,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "starting_date": self.starting_date,
            "total_price": self.total_price,
            "unit_price": self.unit_price,
            "project_id": self.project_id,
            "ms_project_code": self.project_code,
        }
