## Web Scraper API

The searches on the platform only display a few products and use scrolling to load more products. Per page, it only displays 28 products. If pagination is required, it should be noted that the data is retrieved from a GraphQL query. However, since only 15 products need to be displayed, scrolling will load the necessary amount.

Playwright is used because it is a powerful browser automation tool that interacts with web pages like a user would. It can render JavaScript and handle dynamic content that is loaded after the initial HTML response.

### Run

Build docker image

> > docker build -t jumbo_scraper .

Run Container

> > docker run -p 8000:8000 jumbo_scraper

Test

![alt text](image.png)

#### Example 1

Request

```json
{
  "url": "https://www.tiendasjumbo.co/supermercado/despensa/aceite"
}
```

Response

```json
{
  "products": [
    {
      "name": "Aceite Puroil vegetal x3000ml ",
      "price": "$ 22.89",
      "promo_price": "$ 0.0"
    },
    {
      "name": "Aceite Ybarra oliva extra virgen x1L ",
      "price": "$ 63.89",
      "promo_price": "$ 60.695"
    },
    {
      "name": "Aceite Riquisimo garrafa x3000ml ",
      "price": "$ 29.45",
      "promo_price": "$ 0.0"
    },
    {
      "name": "Aceite Premier girasol x2700ml ",
      "price": "$ 52.29",
      "promo_price": "$ 0.0"
    },
    {
      "name": "Aceite Cuisine&Co Mezcla Vegetal x3000Ml ",
      "price": "$ 20.89",
      "promo_price": "$ 19.845"
    },
    {
      "name": "Aceite Ybarra oliva extra virgen x3L ",
      "price": "$ 161.59",
      "promo_price": "$ 153.51"
    },
    {
      "name": "Aceite Bucatti oliva extra virgen x750ml ",
      "price": "$ 53.55",
      "promo_price": "$ 0.0"
    },
    {
      "name": "Aceite Premier girasol x900ml ",
      "price": "$ 18.06",
      "promo_price": "$ 0.0"
    },
    {
      "name": "Aceite Cuisine&Co girasol x3L ",
      "price": "$ 29.99",
      "promo_price": "$ 28.49"
    },
    {
      "name": "Aceite Diana vitaminas x3000ml ",
      "price": "$ 34.02",
      "promo_price": "$ 0.0"
    },
    {
      "name": "Aceite Gourmet Familia multiusos x900ml ",
      "price": "$ 19.86",
      "promo_price": "$ 0.0"
    },
    {
      "name": "Aceite Canola Life puro x3L ",
      "price": "$ 73.69",
      "promo_price": "$ 0.0"
    },
    {
      "name": "Aceite Gourmet familia multiusos x2und x1800ml c-u ",
      "price": "$ 69.9",
      "promo_price": "$ 0.0"
    },
    {
      "name": "Aceite Gourmet Familia multiusos x2600ml ",
      "price": "$ 57.49",
      "promo_price": "$ 0.0"
    },
    {
      "name": "Aceite Oleocali garrafa x3000ml ",
      "price": "$ 29.75",
      "promo_price": "$ 0.0"
    }
  ],
  "url": "https://www.tiendasjumbo.co/supermercado/despensa/aceite"
}
```

#### Example 2

Request

```json
{
  "url": "https://www.tiendasjumbo.co/supermercado/despensa/aceite",
  "num_products": 2
}
```

Response

```json
{
  "products": [
    {
      "name": "Aceite Puroil vegetal x3000ml ",
      "price": "$ 22.89",
      "promo_price": "$ 0.0"
    },
    {
      "name": "Aceite Ybarra oliva extra virgen x1L ",
      "price": "$ 63.89",
      "promo_price": "$ 60.695"
    }
  ],
  "url": "https://www.tiendasjumbo.co/supermercado/despensa/aceite"
}
```
