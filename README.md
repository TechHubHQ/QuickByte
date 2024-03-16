# QuickByte

> NOTE: This project is designed to run only in UNIX/LINUX environment

## Project-Tree

```
QuickByte
├─ .github
│  └─ ISSUE_TEMPLATE
│     ├─ bug_report.md
│     ├─ custom.md
│     └─ feature_request.md
├─ .gitignore
├─ .replit
├─ app.py
├─ Backend
│  ├─ Build
│  │  ├─ QBbRebuildEngine.py
│  │  └─ __init__.py
│  ├─ Connections
│  │  ├─ QBcDBConnector.py
│  │  └─ __init__.py
│  ├─ Controllers
│  │  ├─ QBcrFormCreator.py
│  │  ├─ QBcrUserController.py
│  │  └─ __init__.py
│  ├─ Integration
│  │  ├─ Data
│  │  │  └─ FoodMenu.json
│  │  ├─ QBiLocationIDFetcher.py
│  │  ├─ QBiMenuFetcher.py
│  │  ├─ QBiRestaurantsFetcher.py
│  │  ├─ QBiStdAloneLocFetcher.py
│  │  └─ __init__.py
│  ├─ Logic
│  │  ├─ QBlOrderHandler.py
│  │  ├─ QBlOrderStatusEngine.py
│  │  ├─ QBlPaymentHandler.py
│  │  └─ __init__.py
│  ├─ Models
│  │  ├─ QBmAddressModel.py
│  │  ├─ QBmAdminModel.py
│  │  ├─ QBmLoadLocationID.py
│  │  ├─ QBmLoadMenu.py
│  │  ├─ QBmLoadRestaurantsByID.py
│  │  ├─ QBmNotificationModel.py
│  │  ├─ QBmOrder2ItemModel.py
│  │  ├─ QBmPaymentModel.py
│  │  ├─ QBmUserModel.py
│  │  └─ __init__.py
│  ├─ Services
│  │  ├─ Email
│  │  │  └─ WelcomeEmailTemplate.html
│  │  ├─ QBsLogStorageManager.py
│  │  ├─ QBsWelcomeAlertSender.py
│  │  └─ __init__.py
│  └─ __init__.py
├─ CODE_OF_CONDUCT.md
├─ Config
│  ├─ AppConfig.py
│  └─ __init__.py
├─ Docs
│  ├─ QuickByte.docx
│  ├─ QuickByteGuide.pdf
│  └─ test.txt
├─ Frontend
│  ├─ Static
│  │  ├─ js
│  │  │  ├─ CartRenderer.js
│  │  │  ├─ GetAddress.js
│  │  │  ├─ GetOrders.js
│  │  │  ├─ ImageGetter.js
│  │  │  ├─ MenuDetails.js
│  │  │  ├─ Navbar.js
│  │  │  ├─ OrderStatusTracker.js
│  │  │  ├─ OrderTracker.js
│  │  │  ├─ PaymentProcessor.js
│  │  │  ├─ ProfileSideBar.js
│  │  │  ├─ ProfileUploader.js
│  │  │  ├─ RestaurantGetter.js
│  │  │  ├─ StatesDropdownGetter.js
│  │  │  ├─ SupportDropDownGetter.js
│  │  │  ├─ Swiper.js
│  │  │  ├─ UserLogin.js
│  │  │  └─ UserSignUp.js
│  │  ├─ Json
│  │  │  ├─ Dist_States.json
│  │  │  └─ Support_Issues.json
│  │  └─ styles
│  │     ├─ AddressDetails.css
│  │     ├─ Associate.css
│  │     ├─ Cart.css
│  │     ├─ FAQ.css
│  │     ├─ Help_Center.css
│  │     ├─ Home.css
│  │     ├─ Landing.css
│  │     ├─ Login.css
│  │     ├─ Menu.css
│  │     ├─ MyAddress.css
│  │     ├─ MyOrders.css
│  │     ├─ OrderStatusTracker.css
│  │     ├─ OrderTracker.css
│  │     ├─ Payment.css
│  │     ├─ Profile.css
│  │     ├─ Restaurants.css
│  │     ├─ Settings.css
│  │     └─ SignUp.css
│  └─ Templates
│     ├─ AddressDetails.html
│     ├─ Associate.html
│     ├─ Cart.html
│     ├─ FAQ.html
│     ├─ Help_Center.html
│     ├─ Home.html
│     ├─ Landing.html
│     ├─ Login.html
│     ├─ Menu.html
│     ├─ MyAddress.html
│     ├─ MyOrders.html
│     ├─ OrderStatusTracker.html
│     ├─ OrderTracker.html
│     ├─ Payment.html
│     ├─ Profile.html
│     ├─ Restaurants.html
│     ├─ Settings.html
│     └─ SignUp.html
├─ LICENSE
├─ poetry.lock
├─ pyproject.toml
├─ README.md
├─ requirements.txt
├─ setup.py
└─ Tests
   ├─ FoodMenuApiTest.py
   ├─ OrderStatusTester.py
   └─ __init__.py

```

## TECH-STACK

### Backend
[![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)](https://www.linux.org/)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

### Frontend
![HTML](https://img.shields.io/badge/HTML-239120?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-239120?&style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)

## PRE REQUISITES

    1. Linux -- (VirtualMachine/WSL) 
    2. Python -- (Installed in Linux)
    3. other requirements/libraries will automatically be installed with setup script

## SETUP 

On App start-up run the below command to get the setup done for the APP automatically

 ```bash
 python3 setup.py
 
 # If asked sudo access 
 sudo python3 setup.py
 ```

## Run the APP Locally

-- Run the app with the below command

### Run Prod Server
```bash
nohup python3 app.py --PROD <CORE_DEV>

# If asked for admin access 
nohup sudo python3 app.py  --PROD <CORE_DEV>

# after this check localhost:8080
```

### Run Dev Server
```bash
nohup sudo python3 app.py --debug

# If asked for admin access
nohup sudo python3 app.py --debug

# after this check localhost:5000
```

for running PROD server, you should be part of CORE_DEV team

## Contribution

> Pull this repository
```bash
# If SSH/GPG keys added to GitHub
git clone git@github.com:TechHubHQ/QuickByte.git

# Else
git clone https://github.com/TechHubHQ/QuickByte.git
```

> Create two branches as below
```bash
git branch ACC_<USERNAME>-<BRANCH_NO_OF_USER>_<FEATURE/ISSUE_DESCRIPTION>
git branch <USERNAME>-<BRANCH_NO_OF_USER>_<FEATURE/ISSUE_DESCRIPTION>

# Example
git branch ACC_JOHN-DOE-1_Feature_Description
git branch JOHN-DOE-1_Feature_Description
```

> push the two empty branches first
```bash
git checkout ACC_<USERNAME>-<BRANCH_NO_OF_USER>_<FEATURE/ISSUE_DESCRIPTION>
git push -u origin HEAD

git checkout <USERNAME>-<BRANCH_NO_OF_USER>_<FEATURE/ISSUE_DESCRIPTION>
git push -u origin HEAD
```

> make Changes
```bash
git checkout <USERNAME>-<BRANCH_NO_OF_USER>_<FEATURE/ISSUE_DESCRIPTION>

# make the code changes 
```

> Add the code to Staging
```bash
git gui

# Add only the relevant code files as per branch description in which the code is changes to staging area in gui
```

> Push the code to ACC_branch
```
# In git gui push the code into ACC_<USERNAME>-<BRANCH_NO_OF_USER>_<FEATURE/ISSUE_DESCRIPTION>

# not onto master branch
```

> Create PR
```
# In GitHub create pull request with mentioning anyone of our team member for code review
```

## ISSUES/BUGS
> Please check out .github/ISSUE_TEMPLATE/bug_report.md or custom.md for submitting an issue

## Feature Request
> Please check out .github/ISSUE_TEMPLATE/feature_request.md for submitting as feature request