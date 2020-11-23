# Databases lab2

## Order

| Field       | type    | IsPrimary|
|-------------|---------|---------|
| order\_id   | integer | Primary |
| product\_id | integer |         |
| customer\_id| integer |         |
|payment\_type| integer |         |
| delivery    | boolean |         |
| count       | integer |         |

## Customer

| Field       | type    | IsPrimary|
|-------------|---------|---------|
| customer\_id| integer | Primary |
| seller\_id  | integer |         |
| name        | text    |         |
| surname     | text    |         |
| phone       | text    |         |
| email       | text    |         |

## Seller

| Field       | type    | IsPrimary|
|-------------|---------|---------|
| seller\_id  | integer | Primary |
| name        | text    |         |
| surname     | text    |         |
| salary      | text    |         |

## Product

| Field       | type    | IsPrimary|
|-------------|---------|---------|
| product\_id | integer | Primary |
| name | text |  |
| category       | text    |         |
| price | text | |

## SellerProduct

| Field       | type    | IsPrimary|
|-------------|---------|---------|
| link\_id    | integer | Primary |
| product\_id | integer | |
| seller\_id  | integer | |
