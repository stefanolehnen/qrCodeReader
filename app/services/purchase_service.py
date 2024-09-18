import requests
from bs4 import BeautifulSoup
import re

def scrape_purchase_details(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            shopping_details = {}
            items = []

            # Extração dos detalhes da compra
            datetime_element = soup.find('strong', string=re.compile(r'Emissão:'))
            if datetime_element:
                datetime_text = datetime_element.find_next('strong').text.strip()
                datetime_purchase = re.search(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}', datetime_text)
                shopping_details['datetime_purchase'] = datetime_purchase.group(0) if datetime_purchase else None

            company_name_element = soup.find('div', id='u20')
            shopping_details['company_name'] = company_name_element.text.strip() if company_name_element else None

            total_items_span = soup.find('span', text=re.compile(r'Qtd. total de itens:'))
            shopping_details['total_items'] = total_items_span.find_next_sibling('span').text.strip() if total_items_span else None

            payment_method_span = soup.find('label', text=re.compile(r'Forma de pagamento:'))
            shopping_details['payment_method'] = payment_method_span.find_next_sibling('span').text.strip() if payment_method_span else None

            for item in soup.find_all('tr'):
                produto = {}
                produto_nome = item.find('span', class_='txtTit')
                produto['nome'] = produto_nome.get_text(strip=True) if produto_nome else None
                codigo = item.find('span', class_='RCod')
                produto['codigo'] = codigo.get_text(strip=True).replace('(Código:', '').replace(')', '').strip() if codigo else None
                quantidade = item.find('span', class_='Rqtd')
                produto['quantidade'] = quantidade.get_text(strip=True).replace('Qtde.:', '').strip() if quantidade else None
                unidade = item.find('span', class_='RUN')
                produto['unidade'] = unidade.get_text(strip=True).replace('UN:', '').strip() if unidade else None
                valor_unitario = item.find('span', class_='RvlUnit')
                produto['valor_unitario'] = valor_unitario.get_text(strip=True).replace('Vl. Unit.:', '').strip() if valor_unitario else None
                valor_total = item.find('span', class_='valor')
                produto['valor_total'] = valor_total.get_text(strip=True) if valor_total else None

                if produto:
                    items.append(produto)

            return {
                "shopping_details": shopping_details,
                "products": items
            }
        else:
            return {"error": f"Failed to access URL. Status code: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}
