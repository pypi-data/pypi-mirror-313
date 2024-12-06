# Simple Keenetic client

HTTP client for KeeneticOS-based routers. Uses web interface to connect.
Does not do more than authenticate, fetch SMS messages and mark them as read or delete them.

Example usage:

```python
from simple_keenetic_client import SimpleKeeneticClient

async def get_unread_sms():
  async with SimpleKeeneticClient(
      "http://keenetic-router.test",
      username="testuser",
      password="testpassword",
  ) as client:
      interfaces = await client.get_mobile_interfaces()

      return await self.get_unread_sms(
          interface_names=interfaces.keys()
      )
```

"Real life" usage example: https://github.com/side2k/keensms2mqtt
