#/bin/bash
docker exec api_desweb_cq-desweb_cq-1 sh -c "python manage.py shell < createTables.py"


