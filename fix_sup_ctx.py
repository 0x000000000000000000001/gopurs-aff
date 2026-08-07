import sys

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

import re
content = content.replace("type Supervisor struct {\n\tCancel context.CancelCauseFunc\n\tWg     *sync.WaitGroup\n}", "type Supervisor struct {\n\tCtx    context.Context\n\tCancel context.CancelCauseFunc\n\tWg     *sync.WaitGroup\n}")

content = content.replace("sup := &Supervisor{\n\t\t\tCancel: cancel,\n\t\t\tWg:     &sync.WaitGroup{},\n\t\t}", "sup := &Supervisor{\n\t\t\tCtx:    ctx,\n\t\t\tCancel: cancel,\n\t\t\tWg:     &sync.WaitGroup{},\n\t\t}")

content = content.replace("childCtx, cancel := context.WithCancelCause(context.Background())", """var childCtx context.Context
		var cancel context.CancelCauseFunc
		supAny := ctx.Value(supervisorKey)
		if supAny != nil {
			sup := supAny.(*Supervisor)
			childCtx, cancel = context.WithCancelCause(sup.Ctx)
		} else {
			childCtx, cancel = context.WithCancelCause(context.Background())
		}""")

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
