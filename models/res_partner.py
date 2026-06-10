# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

import requests

class Partner(models.Model):
    _inherit = 'res.partner'

    def guardar_nombre_facturacion_fel(self):
        vat = self.vat
        if self.nit_facturacion_fel:
            vat = self.nit_facturacion_fel

        res = self.obtener_datos_facturacion_fel(vat)
        self.nombre_facturacion_fel = res['nombre']

    def obtener_datos_facturacion_fel(self, vat):
        res = self._datos_sat(self.env.company, vat)
        return res

    def _datos_sat(self, company, nit):
        if nit:
            request_token = "https://felgtaws.digifact.com.gt/gt.com.fel.api.v3/api/login/get_token"
            request_tax_info = "https://felgtaws.digifact.com.gt/gt.com.fel.api.v3/api/SHAREDINFO"
            if company.pruebas_fel:
                request_token = "https://felgttestaws.digifact.com.gt/gt.com.fel.api.v3/api/login/get_token"
                request_tax_info = "https://felgttestaws.digifact.com.gt/gt.com.fel.api.v3/api/SHAREDINFO"

            headers = { "Content-Type": "application/json" }

            data = {
                "Username": company.usuario_fel,
                "Password": company.clave_fel,
            }
            r = requests.post(request_token, json=data, headers=headers)
            token_json = r.json()
            if "Token" in token_json:
                token = token_json["Token"]
                headers_nuevos = {
                    "Content-Type": "applcation/json",
                    "Authorization": token,
                }
                r = requests.get(request_tax_info+'?NIT={}&DATA1=SHARED_GETINFONITcom&DATA2=NIT|{}&COUNTRY=GT&USERNAME={}'.format(company.vat.replace('-','').zfill(12), nit, company.usuario_fel), headers=headers_nuevos)
                certificacion_json = r.json()

                datos_contribuyente = { 'nombre': '', 'nit': '', 'mensaje': '' }
                
                if "RESPONSE" in certificacion_json and len(certificacion_json["RESPONSE"]) > 0:
                    if "NOMBRE" in certificacion_json["RESPONSE"][0]:
                        datos_contribuyente['nombre'] = certificacion_json["RESPONSE"][0]["NOMBRE"]
                        datos_contribuyente['nit'] = certificacion_json["RESPONSE"][0]["NIT"]
                else:
                    datos_contribuyente['mensaje'] = r.text

                return datos_contribuyente
