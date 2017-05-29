# niffler

Installation
------------

```bash
# clone project
cd /path/to/home/dir/of/your/projects
git clone git@github.com:bryazginnn/niffler.git
cd niffler

# create virtualenv
virtualenv -p python3 venv 
source venv/bin/activate
pip install requirements.txt
deactivate
```

Generate user + token
-------------
1. generate token
```bash
echo $RANDOM | shasum
```

2. insert user & token

```
select create_user('<user_name>', 'token_code');
``` 