"""
This module contains the data structures used for requests and responses in the SDK. It defines the payloads
that are sent to and received from the various services.

---
"""


def get_quote_details(quote_number):
    """Builds the xml payload to get the details of a quote from the SAP server.

    Args:
        quote_number (str): The quote number to get details for.

    Returns:
        str: The xml payload to get the details of a quote from the SAP server.
    """
    payload = f"""<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:sap-com:document:sap:rfc:functions">
                   <soap:Header/>
                   <soap:Body>
                      <urn:ZBAPISDQUOTEDETAILSV3>
                         <QUOTATION>{quote_number}</QUOTATION>
                         <RTSTATUS>
                            <!--Zero or more repetitions:-->
                            <item>
                               <TYPE></TYPE>
                               <ID></ID>
                               <NUMBER></NUMBER>
                               <MESSAGE></MESSAGE>
                            </item>
                         </RTSTATUS>
                      </urn:ZBAPISDQUOTEDETAILSV3>
                   </soap:Body>
                </soap:Envelope>"""

    return payload


def list_quotes(sales_org):
    """Builds the xml payload to get all the quotes from a given sales org in the SAP server.

    Args:
        sales_org (str): The sales organization to list quotes for.

    Returns:
        str: The xml payload to get all the quotes from a given sales org in the SAP server.
    """
    payload = f"""<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:sap-com:document:sap:soap:functions:mc-style">
                    <soap:Header/>
                    <soap:Body>
                        <urn:Zbapisdactivequotes>
                            <Salesorganization>{sales_org}</Salesorganization>
                        </urn:Zbapisdactivequotes>
                    </soap:Body>
                </soap:Envelope>"""

    return payload
