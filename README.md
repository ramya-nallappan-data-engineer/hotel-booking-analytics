# Hotel Booking Analytics

A synthetic-data analytics project: Python generators create a connected hotel-booking dataset, DuckDB stores it, and SQL scripts analyse it. It doubles as a practice environment for SQL, data modelling and ETL.

## Dataset

Seven related tables with business relationships between them.

| Dataset | Records |
|---|---:|
| Customers | 500 |
| Hotels | 100 |
| Products | 30 |
| Bookings | 10,000 |
| Payments | 10,000 |
| Reviews | 6,000+ |
| Order items | 13,000+ |

## Workflow

```
Python generators -> CSV files -> DuckDB database -> SQL analytics
                                      |
                              data validation checks
```

## Tech stack

Python, pandas, NumPy, Faker, DuckDB, SQL.

## Quickstart

```bash
git clone https://github.com/ramya-nallappan-data-engineer/hotel-booking-analytics.git
cd hotel-booking-analytics
pip install -r requirements.txt
python main.py        # generates the seven CSV files into data/
```

`database/` contains the DuckDB loading, validation and query scripts, and `schema/schema.sql` defines the tables.

## Repository layout

```
generators/   Synthetic data generators, one per table
database/     DuckDB creation, loading, validation and query helpers
schema/       Table definitions
sql/          Analytical SQL scripts
data/         Generated CSV files
main.py       Runs all generators
config.py     Generation settings
```

## Roadmap

- [ ] Analytical SQL views and a query library
- [ ] Dashboard on top of the DuckDB data
- [ ] dbt models
- [ ] Airflow orchestration
- [ ] Docker support
- [ ] GitHub Actions CI

## License

MIT
