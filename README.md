# Flask template for quick start

Work in progress

Template was made to easily add UI for users to run Python scripts without *.bat files and all this staff  and to make easy to change master-data in data base

Html pages are based on bootstrap v5.1.1

Based on MySQL

To do:
1. Admin page to administrate users
2. Change data in database via uploading xlsx files
3. Run scripts with progress-bar shown to user

Done:
1. User role-based auth


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
To change items per page in pagination change PAGINATION_ITEMS parameter in hq/__init__.py