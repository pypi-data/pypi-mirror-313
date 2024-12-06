from typing import Any, Optional
from dotenv import load_dotenv
from os import getenv
import json
import urllib.parse
import requests
from OTCFinUtils.security import get_dataverse_token
from OTCFinUtils.data_structs import (
    APIParams, 
    HTTPMethod, 
    HTTPStatus, 
    ResponseIds,
)
from OTCFinUtils.utils import (
    extract_segment_response_id, 
    extract_segment_status_code, 
    extract_segment_table_name
)


class DVHandler:
    _BATCH_BOUNDARY: str = "batch_boundary"
    _BATCH_CHUNK_SIZE: int = 900
    _NEXT_PAGE_KEY: str = "@odata.nextLink"
    _instance = None


    def __new__(cls, dataverse_url: Optional[str] = None, user_id: Optional[str] = None) -> "DVHandler":
        if dataverse_url is None:
            load_dotenv()
            dataverse_url = getenv("DATAVERSE_DEFAULT_URL", "")

        if not cls._instance:
            cls._instance = super(DVHandler, cls).__new__(cls)
            cls._instance.__init__(dataverse_url, user_id)
        
        return cls._instance # type: ignore
    

    def __init__(self, dataverse_url: str, user_id: Optional[str] = None) -> None:
        self.api_url = f"{dataverse_url}/api/data/v9.2"
        self.token = get_dataverse_token(dataverse_url)
        self.headers = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
        self.user_id = user_id


    def get_entities_list(self, table: str, filter: Optional[str] = None, select: Optional[str] = None, expand: Optional[str] = None) -> list[dict]:
        api_url = self._create_url(table, select, filter, expand)
        response = requests.get(api_url,headers=self.headers)
        
        if not response.status_code == HTTPStatus.OK.value:
            raise RuntimeError(f"Could not query entities for: {table}. Error: {response.text}")
        
        response_data = response.json()
        entities: list[dict] = response_data["value"]

        if DVHandler._NEXT_PAGE_KEY in response_data:
            next_page_link = response_data[DVHandler._NEXT_PAGE_KEY]
            next_page_entities = self.get_next_page(next_page_link)
            entities.extend(next_page_entities)
        
        return entities
    

    def _create_url(self, domain: str|None=None, select: str|None=None, filter: str|None=None, expand: str|None=None) -> str:
        """
        A general helper function. Can be used extensively.
        """
        url = f"{self.api_url}/{domain}?"
        params = []
        params.append(f"$select={select}") if select else None
        params.append(f"$filter={urllib.parse.quote(filter)}") if filter else None
        params.append(f"$expand={expand}") if expand else None
        url += "&".join(params)
        return url
    

    def get_next_page(self, page_link: str) -> list[dict]:
        response = requests.get(page_link, headers=self.headers)

        if response.status_code != HTTPStatus.OK.value:
            raise RuntimeError(f"Cannot get page data for link: {page_link}.")

        page_data = response.json()
        entities: list[dict] = page_data["value"]
        
        if DVHandler._NEXT_PAGE_KEY in page_data:
            next_page_link = page_data[DVHandler._NEXT_PAGE_KEY]
            next_page_entities = self.get_next_page(next_page_link)
            entities.extend(next_page_entities)
        
        return entities
    

    @staticmethod
    def create_expand_query_string(lookup_name: str, select: Optional[str]=None, filter: Optional[str]=None) -> str:
        params = []
        
        if select:
            select = f"$select={select}"
            params.append(select)
        if filter:
            filter = f"$filter={filter}"
            params.append(filter)
        
        params = ";".join(params)

        return f"{lookup_name}({params})"
    

    def get_table_definition(self, table: str, fields: Optional[str] = None) -> dict:
        """
        Returns the table definition information of the given table.
        """
        url = self._create_url(f"EntityDefinitions(LogicalName='{table}')", fields)
        response = requests.get(url=url, headers=self.headers)

        if response.status_code != HTTPStatus.OK.value:
            raise RuntimeError(f"Could not get table definition: {response.text}")

        return response.json()
    

    # TODO - review and test this function
    
    def get_columns_names(self, table_name: str) -> list[str]:
        expand = "Attributes($select=DisplayName,LogicalName,AttributeType,SchemaName),"
        expand += "Keys($select=KeyAttributes)"
        
        url = self._create_url(
            domain=f"EntityDefinitions(LogicalName='{table_name}')",
            select="LogicalName",
            filter=None,
            expand=expand,
        )
 
        response = requests.get(url, headers=self.headers)
        keys = []
        
        if response.status_code != HTTPStatus.OK.value:
            raise RuntimeError(f"Could not get column names for {table_name}. Response: {response.text}")
        
        data = response.json()
        keysData = data.get("Keys", [])
        for item in keysData:
            if "KeyAttributes" in item:
                keys.extend(item["KeyAttributes"])  

        attributes = data.get("Attributes", [])
        filtered_attributes = []
        
        for attribute in attributes:
            if not attribute["LogicalName"].startswith("new_") and not attribute["LogicalName"] == "statecode":
                continue

            if "DisplayName" not in attribute or not attribute["DisplayName"]:
                continue

            display_name_field = attribute["DisplayName"]
            
            if (
                "UserLocalizedLabel" not in display_name_field or 
                not display_name_field["UserLocalizedLabel"] or 
                not display_name_field["UserLocalizedLabel"]["Label"]
            ):
                continue

            is_key = attribute["LogicalName"] in keys
            is_lookup = attribute["AttributeType"] == "Lookup"
            is_choice = attribute["AttributeType"] == "Picklist"
            is_bool = attribute["AttributeType"] == "Boolean"
            
            lookup_table_name = None
            lookup_column_name = None
            lookup_relationship = None
            
            choice_name = None
            choice_default_value= None
            choice_dictionary= None
            
            if is_lookup:
                lookup_details = self.get_lookup_details(
                    table_name, attribute["LogicalName"]
                )
                lookup_table_name = lookup_details["lookup_table_name"]
                lookup_column_name = lookup_details["lookup_column_name"]
                lookup_relationship = lookup_details["lookup_relationship"]
            
            elif is_choice:
                choice_details = self.get_choice_details(table_name, attribute["LogicalName"])
                choice_name = choice_details["choice_name"]
                choice_default_value= choice_details["choice_default_value"]
                choice_dictionary= choice_details["choice_dictionary"]
            
            elif is_bool:  
                bool_dct= []
                bool_dct.append({"Value": True, "DV_Display": "Yes", "Excel_Value": "Yes"})
                bool_dct.append({"Value": False, "DV_Display": "No", "Excel_Value": "No"})
                choice_dictionary= json.dumps(bool_dct)
            
        
            filtered_attributes.append({
                "LogicalName": attribute["SchemaName"] if is_lookup else attribute["LogicalName"],
                "DisplayName": attribute["DisplayName"]["UserLocalizedLabel"]["Label"],
                "AttributeType": attribute["AttributeType"],
                "IsKey": is_key,
                "IsLookup": is_lookup,
                "LookupRelationship":lookup_relationship,
                "LookupTable": lookup_table_name,
                "LookupColumn": lookup_column_name,
                "IsChoice": is_choice,
                "ChoiceName": choice_name,
                "ChoiceDefaultValue": choice_default_value,
                "ChoiceDictionary": choice_dictionary,
            })

        return filtered_attributes
        

    # TODO - review and test this function
    
    def get_lookup_details(self, table_name: str, logical_name: str) -> dict:
        url = self._create_url(
            domain=f"EntityDefinitions(LogicalName='{table_name}')/ManyToOneRelationships",
            select="ReferencedEntityNavigationPropertyName,ReferencedEntity,ReferencedAttribute,ReferencingAttribute",
            filter=f"ReferencingAttribute eq '{logical_name}'"
        )

        response = requests.get(url, headers=self.headers)

        if response.status_code != HTTPStatus.OK.value:
            raise RuntimeError(f"Could not get lookup details for {table_name}. Response: {response.text}")
        
        data = response.json()
        if not data["value"]:
            raise RuntimeError(f"No data received for {table_name}")
        
        relationship = data["value"][0]
        lookup_table_name = relationship["ReferencedEntity"]
        lookup_relationship = relationship["ReferencedEntityNavigationPropertyName"]

        key_url = self._create_url(
            domain=f"EntityDefinitions(LogicalName='{lookup_table_name}')/Keys",
            select="KeyAttributes",
        )
        key_response = requests.get(key_url, headers=self.headers)
        lookup_column_name = None
        
        if key_response.status_code != HTTPStatus.OK.value:
            raise RuntimeError(f"Could not get lookup details for {table_name}. Response: {key_response.text}")
        
        key_data = key_response.json()
        if not key_data["value"]:
            raise RuntimeError(f"Could not get lookup details for {table_name}. No 'value' field in response.")

        keys_data = key_data["value"][0]                    
        lookup_column_name = str(keys_data["KeyAttributes"])

        return {
            "lookup_table_name": lookup_table_name,
            "lookup_column_name": lookup_column_name,
            "lookup_relationship": lookup_relationship,
        }
        

    # TODO - review and test this function
    
    def get_choice_details(self, table_name: str, logical_name: str) -> dict:
        url = f"{self.api_url}/EntityDefinitions(LogicalName='{table_name}')"
        url += f"/Attributes(LogicalName='{logical_name}')"
        url += "/Microsoft.Dynamics.CRM.PicklistAttributeMetadata?"
        url += "$select=LogicalName,DefaultFormValue&"
        url += "$expand=GlobalOptionSet($select=Name,Options)"
        
        response = requests.get(url, headers=self.headers)
        choice_default_value =  None
        
        if response.status_code != HTTPStatus.OK.value:
            raise RuntimeError(f"Could not get choice details for {table_name}. Response: {response.text}")
        
        data = response.json()
        if data["DefaultFormValue"]:
            choice_default_value =  None if data["DefaultFormValue"]  == -1 else data["DefaultFormValue"] 
        
        if not data["GlobalOptionSet"]:
            raise RuntimeError(f"Could not get choice details for {table_name}. Global Option Set = {data['GlobalOptionSet']}")
        
        choice = data["GlobalOptionSet"]
        choiceName = choice["Name"]
        choiceOptions = choice["Options"]

        result = []
        
        for option in choiceOptions:
            result.append({
                "Value": option["Value"], 
                "DV_Display": option["Label"]["UserLocalizedLabel"]["Label"],
                "Excel_Value": option["Label"]["UserLocalizedLabel"]["Label"]}
            ) 
        
        json_result = json.dumps(result) 
        
        return {
            "choice_name": choiceName,
            "choice_default_value": choice_default_value,
            "choice_dictionary": json_result
        }
        
    
    def upsert_bulk(self, data: list[dict], no_response=False) -> ResponseIds:
        """
        Executes a bulk upsert operation.
        If the data has an id, then update the entity.
        If the data has no id, then insert the entity.

        If there are more than items than the chunk size, 
        splits the operation into multiple batches.
        """
        response_ids = ResponseIds()
        
        for i in range(0, len(data), DVHandler._BATCH_CHUNK_SIZE):
            from_index = i
            to_index = min(len(data),i + DVHandler._BATCH_CHUNK_SIZE)
            subset_data = data[from_index : to_index]
            subset_response_ids = self._upsert_bulk_subset(subset_data, no_response=no_response)
            response_ids.merge(subset_response_ids)
            
        return response_ids

    
    def _upsert_bulk_subset(self, data: list[dict], no_response=False) -> ResponseIds:
        """
        Used as a helper function for the main bulk-upsert function.
        """
        batch_params: list[APIParams] = []
        id_columns: list[str] = []
        
        for record in data:
            entity_id = record.pop("entity_id")
            table_name: str = record.pop("table_name")
            id_column: str = record.pop("id_column", "")
            id_columns.append(id_column)
            
            if entity_id:
                item_url = self._create_url(domain=f"{table_name}({entity_id})", select=id_column)
                method = HTTPMethod.PATCH.value
            else:
                item_url = self._create_url(domain=table_name, select=id_column)
                method = HTTPMethod.POST.value
            
            record_params = APIParams(url=item_url, method=method, data=record)
            batch_params.append(record_params)

        batch_response = self._execute_batch_operation(batch_params)
        if no_response:
            return ResponseIds()
        
        response_ids = DVHandler._extract_response_ids(batch_response, id_columns)
        
        return response_ids
    
    
    @staticmethod
    def _extract_response_ids(batch_response: str, id_columns: list[str]) -> ResponseIds:
        """
        From the batch response string, returns the ids of the
        created / updated entities in a ResponseIds object, only
        if the id column names are provided.
        """
        response_ids = ResponseIds()
        response_parts = batch_response.split("--batchresponse")
        response_parts = response_parts[1:-1]
        
        for response_part, id_column in zip(response_parts, id_columns):
            response_lines = response_part.split("\n")
            object_id: Optional[str] = extract_segment_response_id(response_lines, id_column)
            status_code: int = extract_segment_status_code(response_lines)
            table: str = extract_segment_table_name(response_lines)
            
            if object_id:
                response_ids.append(status_code, object_id, table)

        return response_ids
    
    
    def _execute_batch_operation(self, batch_params: list[APIParams]) -> str:
        """
        A general helper function. Can be used for any type of batch operation.
        """
        headers = {
            'Authorization': f'Bearer {self.token}', 
            'Content-Type': f'multipart/mixed;boundary={DVHandler._BATCH_BOUNDARY}',
            "Prefer": 'odata.continue-on-error',
        }
        batch_strings = []
        for curr_params in batch_params:
            try:
                batch_string = self._create_batch_item_string(
                    DVHandler._BATCH_BOUNDARY, 
                    curr_params.method, 
                    curr_params.url,
                    curr_params.data,
                )
                batch_strings.append(batch_string)
            except Exception as e:
                raise RuntimeError(f"Failed to create batch item: {str(e)}")
        
        batch_strings.append(f"--{DVHandler._BATCH_BOUNDARY}--")
        batch_body = "\n".join(batch_strings) + "\r\n"

        api_url = f"{self.api_url}/$batch"
        response = requests.post(api_url, data=batch_body, headers=headers)

        if response.status_code == HTTPStatus.OK.value:
            return response.text
        else:
            raise RuntimeError(f"Batch operation was not successful: {response.text}")
  
  
    def _create_batch_item_string(self, boundary: str, method: str, url: str, data: dict | None = None) -> str:
        """
        A helper function for creating the batch request body.
        """
        batch_item_string = (
            f"--{boundary}\n"                      
            "Content-Type: application/http\n"     
            "Content-Transfer-Encoding: binary\n\n"
            f"{method} {url} HTTP/1.1\n"           
        )

        headers = [
            f"Authorization: Bearer {self.token}",
            "Content-Type: application/json",
            'Prefer: return=representation',
        ]
        
        if self.user_id is not None:
            headers.append(f"CallerObjectId: {self.user_id}")
        
        headers = "\n".join(headers)
        batch_item_string += f"{headers}\n\n"

        if data:
            batch_item_string += json.dumps(data)
        
        return batch_item_string

    
    def get_by_id(self, table_name: str, dataverse_id: str) -> dict:
        dv_url = f"{self.api_url}/{table_name}({dataverse_id})"
        response = requests.get(dv_url,headers=self.headers)
        if response.status_code != HTTPStatus.OK.value:
            raise RuntimeError(f"Could not get entity by id: {dataverse_id}. Response: {response.text}")
        return response.json()
        

    def delete_entities(self, data: list[dict]) -> str:
        """
        A generic function for bulk-deleting entities 
        based on the provided list of dictionaries.
        """
        batch_params: list[APIParams] = []
        
        for record in data:
            table: str = record.pop("table")
            record_id: str = record.pop("id")
            
            url = self._create_url(f"{table}({record_id})")
            record_params = APIParams(url, "DELETE")
            
            batch_params.append(record_params)

        batch_response = self._execute_batch_operation(batch_params)
        
        return batch_response


def get_dv_handler() -> DVHandler:
    return DVHandler.__new__(DVHandler)


def set_up_dv_handler(dataverse_url: str) -> DVHandler:
    return DVHandler.__new__(DVHandler, dataverse_url)