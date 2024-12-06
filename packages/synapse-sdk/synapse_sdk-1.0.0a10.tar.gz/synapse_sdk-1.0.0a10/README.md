This is the SDK to develop synapse plugins


## Internationalization

### Find Messages
```bash
 $ find . -name "*.py" | xargs xgettext -o messages.pot
```

### Make Messages
```bash
 $ msginit -l ko -i messages.pot -o synapse_sdk/locale/ko/LC_MESSAGES/messages.po
 $ msginit -l en -i messages.pot -o synapse_sdk/locale/en/LC_MESSAGES/messages.po
```

### Compile Messages

```bash
 $ msgfmt synapse_sdk/locale/ko/LC_MESSAGES/messages.po -o synapse_sdk/locale/ko/LC_MESSAGES/messages.mo
 $ msgfmt synapse_sdk/locale/en/LC_MESSAGES/messages.po -o synapse_sdk/locale/en/LC_MESSAGES/messages.mo
```
