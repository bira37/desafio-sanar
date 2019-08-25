# -*- coding: utf-8 -*-

"""
    mundiapi

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io ).
"""

import mundiapi.models.create_apple_pay_header_request

class CreateApplePayRequest(object):

    """Implementation of the 'CreateApplePayRequest' model.

    The ApplePay Token Payment Request

    Attributes:
        version (string): The token version
        data (string): The cryptography data
        header (CreateApplePayHeaderRequest): The ApplePay header request
        signature (string): Detached PKCS #7 signature, Base64 encoded as
            string
        merchant_identifier (string): ApplePay Merchant identifier

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "version":'version',
        "data":'data',
        "header":'header',
        "signature":'signature',
        "merchant_identifier":'merchant_identifier'
    }

    def __init__(self,
                 version=None,
                 data=None,
                 header=None,
                 signature=None,
                 merchant_identifier=None):
        """Constructor for the CreateApplePayRequest class"""

        # Initialize members of the class
        self.version = version
        self.data = data
        self.header = header
        self.signature = signature
        self.merchant_identifier = merchant_identifier


    @classmethod
    def from_dictionary(cls,
                        dictionary):
        """Creates an instance of this model from a dictionary

        Args:
            dictionary (dictionary): A dictionary representation of the object as
            obtained from the deserialization of the server's response. The keys
            MUST match property names in the API description.

        Returns:
            object: An instance of this structure class.

        """
        if dictionary is None:
            return None

        # Extract variables from the dictionary
        version = dictionary.get('version')
        data = dictionary.get('data')
        header = mundiapi.models.create_apple_pay_header_request.CreateApplePayHeaderRequest.from_dictionary(dictionary.get('header')) if dictionary.get('header') else None
        signature = dictionary.get('signature')
        merchant_identifier = dictionary.get('merchant_identifier')

        # Return an object of this model
        return cls(version,
                   data,
                   header,
                   signature,
                   merchant_identifier)


