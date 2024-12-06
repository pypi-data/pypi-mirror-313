# ovos-PHAL-plugin - system

Provides system specific commands to OVOS.
The dbus interface for this plugin is not yet established.

# Install

`pip install ovos-PHAL-plugin-system`

# Config

This plugin is a Admin plugin, it needs to run as root and to be explicitly enabled in mycroft.conf

```javascript
{
"PHAL": {
    "admin": {
        "ovos-PHAL-plugin-system": {"enabled": true}
    }
}
}
```
if not enabled (omit config above) it will be run as the regular user, you need to ensure [polkit policy](#) is set to allow usage of systemctl without sudo.  Not yet implemented


handle bus events to interact with the OS

```python
self.bus.on("system.ntp.sync", self.handle_ntp_sync_request)
self.bus.on("system.ssh.status", self.handle_ssh_status)
self.bus.on("system.ssh.enable", self.handle_ssh_enable_request)
self.bus.on("system.ssh.disable", self.handle_ssh_disable_request)
self.bus.on("system.reboot", self.handle_reboot_request)
self.bus.on("system.shutdown", self.handle_shutdown_request)
self.bus.on("system.factory.reset", self.handle_factory_reset_request)
self.bus.on("system.factory.reset.register", self.handle_reset_register)
self.bus.on("system.configure.language", self.handle_configure_language_request)
self.bus.on("system.mycroft.service.restart", self.handle_mycroft_restart_request)
```
