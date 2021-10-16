# Flask template for quick start

Work in progress

Template was made to easily add UI for users to run Python scripts without *.bat files and all this staff  and to make easy to change master-data in data base

Html pages are based on bootstrap v5.1.1

Based on FLASK and MySQL

Done:
1. User role-based auth
2. Simple UI to run scripts with data from form
3. Upload data from Excel, view data on page, download data via Excel


## Steps to do
<ol>
    <li>Go to hq/__init__.py and change:
        <ul>
            <li>app.secret_key</li>
            <li>MYSQL_HOST</li>
            <li>MYSQL_USER</li>
            <li>MYSQL_PASSWOR</li>
            <li>MYSQL_DB (database should be already created)</li>
        </ul>
    </li>
    <li>
        Run script db_setup.py. It will create first admin user
    </li>
</ol>

## Important
Temporary files stored in hq/static/tmp_files/**<br>
You need to create cron task to clear this folder on your server
