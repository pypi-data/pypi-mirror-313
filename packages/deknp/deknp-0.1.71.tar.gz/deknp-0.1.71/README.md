Merge shared dependencies and update package.json

```shell
# enter project dir which contains a package.json

# generate shell scripts and run them
deknp shell .

# just like npm install
deknp install

# generate server
deknp server
# update dv3/requests
deknp install

# publish current package
deknp sure
npm publish

# env vars
# change env
deknp env to dev
# load settings from os.environ
deknp env final
```
