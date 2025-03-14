
# My Food Project

## Built with

- [Python](https://www.python.org/) - Programming Language, version 3.13
- [PostgreSQL](https://www.postgresql.org/) Open-source relational database management system, version 15.
- [Django](https://www.djangoproject.com/) - High-level Python web framework
- [Django Rest Framework](https://www.django-rest-framework.org/) - Powerful and flexible toolkit for building Web APIs
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation

## Prerequisites

This project requires Python (preferably version 3.13) and the latest PostgreSQL.
To check if they are available on your machine, try running the following commands.

### Python Installation

#### macOS

It is recommended to install the latest version using Homebrew, although macOS often comes with Python pre-installed.

1. **Install Homebrew** (if not already installed):
   <a name="brew-installation"></a>
   
   Homebrew is a package manager for macOS that simplifies installing and managing software.

   Open Terminal and run:

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python** (if not already installed):

   ```bash
   brew install python@3.13
   ```

#### Linux Installation

Python is typically pre-installed on most Linux distributions. However, we need 3.13 version, follow these steps.

1. **Update the Package List**:

   For Debian-based distributions (e.g., Ubuntu), run:

   ```bash
   sudo apt update
   ```

2. **Install Python**:

   ```bash
   sudo apt install python3.13 python3.13-venv
   ```

#### Windows Installation

1. **Download Python Installer**:

   Visit the official Python website and download the Python 3.13 installer for Windows:

   [Download Python](https://www.python.org/downloads/)

2. **Run the Installer**:

   - Open the downloaded file.
   - Ensure that the option **"Add Python to PATH"** is checked.
   - Select **"Install Now"** and follow the prompts.

---

#### Verifying Python Installation

Regardless of your operating system, verify that Python has been installed correctly by running:

```bash
python3 --version
```

Or on Windows (if Python 3 is the default):

```bash
python --version
```

You should see the installed version number, e.g.:

```bash
Python 3.13
```

### PostgreSQL Installation

#### macOS

1. **Install Homebrew** (if not already installed):

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install PostgreSQL**:

   ```bash
   brew install postgresql
   ```

3. **Start PostgreSQL**:

   ```bash
   brew services start postgresql
   ```

4. **Verify the installation**:

   ```bash
   psql --version
   ```

#### Linux Installation

1. **Update the package list**:

   ```bash
   sudo apt update
   ```

2. **Install PostgreSQL**:

   ```bash
   sudo apt install postgresql postgresql-contrib
   ```

3. **Start PostgreSQL**:

   ```bash
   sudo systemctl start postgresql
   ```

4. **Verify the installation**:

   ```bash
   psql --version
   ```

#### Windows Installation

1. Download the PostgreSQL installer from [EnterpriseDB](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads).

2. Run the installer and follow the on-screen instructions. Make sure to note down the username (`postgres`) and password during installation.

3. After installation, the PostgreSQL service should start automatically. If not, you can start it manually:
   - Go to **Start** > **PostgreSQL** > **Start PostgreSQL**.

4. **Verify the installation**:

   Open the command prompt and run:

   ```bash
   psql --version
   ```


## Project Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/snbby/MyFood.git
    cd myfood
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv .venv
    ```

3. **Activate the virtual environment:**
   <a name="activate-venv"></a>
   ### macOS/Linux:

    ```bash
    source .venv/bin/activate
    ```

   ### Windows:

    ```bash
    .venv\Scripts\activate
    ```

4. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

5. Access PostgreSQL, create postgres database, user and password, exit
   ```bash
   psql postgres
   CREATE DATABASE your_db_name;
   CREATE USER your_db_user_name WITH PASSWORD 'your_db_password';
   GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
   \q
   ```

6. **Set the following values to your environment variables.**
   <a name="enviroment-variables"></a>
   
   Do not forget about `MYFOOD_DEBUG=True` variable. You can choose
   the language [to your taste](http://www.i18nguy.com/unicode/language-identifiers.html). 
   Print them in your terminal session:

   ```bash
   export MYFOOD_DATABASE_NAME=your_db_name
   export MYFOOD_DATABASE_USER=your_db_user_name
   export MYFOOD_DATABASE_PASS=your_db_password
   export MYFOOD_DEBUG=True
   export MYFOOD_LANGUAGE=en-US
   ```
   
   Alternatively, you can create a shell script (set_env.sh), which is more convenient to use each time rather than 
   manually printing environment variables in the terminal every time you need it.
   
   ```bash
   # Set environment variables
   export MYFOOD_DATABASE_NAME=your_db_name
   export MYFOOD_DATABASE_USER=your_db_user_name
   export MYFOOD_DATABASE_PASS=your_db_password
   export MYFOOD_DEBUG=True
   export MYFOOD_LANGUAGE=en-US
   
   # Print to verify
   echo "Environment variables set:"
   echo "Database Name: $MYFOOD_DATABASE_NAME"
   echo "Database User: $MYFOOD_DATABASE_USER"
   echo "Database Password: $MYFOOD_DATABASE_PASS"
   echo "Debug Mode: $MYFOOD_DEBUG"
   echo "Language: $MYFOOD_LANGUAGE"
   ```
   Make the script executable:
   ```bash
   chmod +x set_env.sh
   ```
   
   Run the script:
   ```bash
   source ./set_env.sh
   ```

7. Apply migrations:

    ```bash
    python manage.py migrate
    ```
   
    They stored at `myfood/migrations/`

8. Create superuser in Django:

   ```bash
   python manage.py createsuperuser
   ```

9. You will be prompted to enter the following details:

   - Username: The desired username for the superuser.
   - Email address: The email address of the superuser.
   - Password: Your chosen password (you will be asked to confirm it).

   Once you have entered the details, Django will create the superuser account.

10. Run the server:
    ```bash
    python manage.py runserver
    ```
11. Log into the Django admin interface

Log into the Django admin interface at `http://127.0.0.1:8000/admin/` using the superuser credentials.

## Uploading food data to DB

1. Download data dump of all food:
   On Linux is wget(it is preinstalled)
   ```bash
   wget -O eng_products.csv.gz https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv.gz 
   ```
   
   On macOS you should install wget before downloading data dump using [brew](#brew-installation) that was installed before.
   ```bash
   brew install wget
   ```
   
   On Windows you can install [Wget for Windows](https://gnuwin32.sourceforge.net/packages/wget.htm) to perform this command.
   
2. **Unpack it to `artifacts/myfood`**

   You can use `gunzip` on macOS/Linux, it is typically pre-installed.
   ```bash
   gunzip -c eng_products.csv.gz > artifacts/myfood/eng_products.csv
   ```
   
   Use Git Bash for Windows which is installed automatically when you install Git on Windows.
   Alternatively, you can use [7-Zip](https://www.7-zip.org/) on Windows.

3. Be sure that you have set enviromental variables as in [Step 6](#enviroment-variables) and 6 of the [Project Installation](#project-installation).

4. Activate your virtual enviroment as in [Step 3](#activate-venv) and 6 of the [Project Installation](#project-installation).
5. Migrate database:

   ```bash
   python manage.py migrate
   ```
6. Launch uploading data to db:

   ```bash
   python manage.py food_to_db
   ```

7. ???
8. Wait approximately 90 minutes...
9. PROFIT!
 