# mortgage_simulator
Mortgage Simulation Library for you to simulate and track your mortgage progress

## installation instructions

1. clone the repo
```
git clone git@github.com:fafnirZ/MortgageSim.git
cd MortgageSim
```

2. init the venv and install dependencies
```
make venv
make develop
```

3. run the streamlit app
```
make run
```

## Other info
once you make changes to the parameters, the state is stored in a base64 encoded json updated in your URL
so if you save this URL and paste it in the next time you restart the app, it should give you the same state as last time

