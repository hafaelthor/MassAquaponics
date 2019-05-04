# Issues in Mass Aquaponics
## IoT App
### Database Models
#### Community Broker
1. I really want to make the CharFields of name and host non-empty. I've tried to set blank=False to use MinLengthValidator(1) etc. but it doesn't seem to work.
### Consumers
#### Community Broker Consumer
1. I'm not sure if the is_connected flag is actually working.
2. I never tested a reconnection, maybe the is_initialized flag should be a is_connecting flag so the loop won't try to repeatedly reconnect "overflowing" the connection function (if that's
a thing).
## Transpiler
### WebPack Configuration
1. I haven't tested all possible cases of the bundle generations
## Node Module
### NPM Audit
1. When installing the dependencies for webpack and for the frontend code, npm found a high severity vulnerability. To see it, run:
    ```
    $ npm audit #on the /src/ folder
    ```
    output:
    ```

                        === npm audit security report ===

    ┌──────────────────────────────────────────────────────────────────────────────┐
    │                                Manual Review                                 │
    │            Some vulnerabilities require your attention to resolve            │
    │                                                                              │
    │         Visit https://go.npm.me/audit-guide for additional guidance          │
    └──────────────────────────────────────────────────────────────────────────────┘
    ┌───────────────┬──────────────────────────────────────────────────────────────┐
    │ High          │ Arbitrary File Overwrite                                     │
    ├───────────────┼──────────────────────────────────────────────────────────────┤
    │ Package       │ tar                                                          │
    ├───────────────┼──────────────────────────────────────────────────────────────┤
    │ Patched in    │ >=4.4.2                                                      │
    ├───────────────┼──────────────────────────────────────────────────────────────┤
    │ Dependency of │ node-sass [dev]                                              │
    ├───────────────┼──────────────────────────────────────────────────────────────┤
    │ Path          │ node-sass > node-gyp > tar                                   │
    ├───────────────┼──────────────────────────────────────────────────────────────┤
    │ More info     │ https://npmjs.com/advisories/803                             │
    └───────────────┴──────────────────────────────────────────────────────────────┘
    found 1 high severity vulnerability in 7765 scanned packages
    1 vulnerability requires manual review. See the full report for details.
    ```
    1. It's currently an [open issue](https://github.com/sass/node-sass/issues/2625) in the node-sass repository.
    2. It has generated a [pull request](https://github.com/nodejs/node-gyp/pull/1718) in node-gyp and another [open issue](https://github.com/npm/node-tar/issues/212) in node-tar.