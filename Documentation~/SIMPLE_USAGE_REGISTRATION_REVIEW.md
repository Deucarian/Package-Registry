# Simple usage registration review

The approved convenience APIs expose short calls for the application's default
notification area, theme audio output, screen router, and object loader. Each
facade holds exactly one borrowed registration. This deliberately introduces
one mutable static field per facade, recorded as a version-specific exception.

The domain state and behavior remain in scoped instances: `NotificationService`,
`DeucarianThemeAudioPlayer`, `IUIFlowRouter`, and `ObjectLoadingHost`. The facade
does not duplicate their state, create services on demand, search scenes, or
select arbitrary services by type. Calls before configuration fail clearly.
Other instances remain usable independently of the application default.

The host or application composition code owns setup and teardown. Binding rejects
an existing active registration. Disposing an old registration cannot clear a
newer binding. The registration never disposes the borrowed domain owner. Unity
facades reset at subsystem registration and scene hosts unregister when disabled;
the pure notification facade is bound and unbound explicitly by its owner.

The allowance is one field for each exact assembly, type, and current package
version in `architecture-metrics-exceptions.json`. It does not permit additional
global collections or mutable domain state. The normal size and responsibility
limits remain unchanged; version changes require another review.

Persistence, selection, lists, commands, sessions, authentication, spawning,
projectiles, and progression use explicitly supplied hosts or profiles. They do
not receive new static registrations. The object-loading byte adapter is a
separate collaborator so the pipeline stays within its normal type-size budget.

Validation includes duplicate and stale-registration tests, host teardown tests,
scoped ownership tests, all package validators, and architecture metrics against
these exact exceptions. No baseline rewrite or scanner exclusion is introduced.
