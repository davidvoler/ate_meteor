Fixture API
-----------
TestStatus (idle/running/stopped/error)
DoorStatus (open/closed/error)

Cavity/UUT API
--------------
ConnectedUUT - identify which uut is in which cavity

Test API
--------
TestStarted (testId, cavity, uut)
TestCompleted (TestId, cavity, uut, status/error/verdict)
TestResults(testId, cavity, uut, results)

Notification API
----------------
FixtureHealth
CavityHealth

Resources api
-------------
Some test may require hardware resource to be in a specific state.
Other tests require a sole use of the resource making sure that the resource is not used by any other uut.

AcquireLock (resource)
ReleaseLock(resource)
GetResourceStatus(resource)
SetResourceState(resource, state)

