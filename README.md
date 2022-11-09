# prova verzel full stack

## requesitos obrigatorios
```
python
pip
aws-cli
```

## requesitos não obrigatorios
```
terraform
```

## env
crie um arquivo .env em store
```bash
TOKEN_PASS=
ACCESS_KEY=
SECRETE_KEY=
BUCKET=
REGION=
```

## executando 

crie um virtual env
```bash
python -m venv env
```

instale os packages
```bash
pip install -r requirements.txt
```

execute
```bash
python3 store/manage.py runserver
```

## terraform
```
para agilizar o processo o tem um script terraform para criar um bucket na s3  
```

devera ter o aws-cli configurado, será usado o profile ```default``` se quiser pode mudar no ```main.tf```

```bash
$ terraform init
$ terraform plan
$ terraform apply
```


