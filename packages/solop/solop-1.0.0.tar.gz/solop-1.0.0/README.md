# SoloP

SoloP will be a tool that can be used to manage a Solo Developers tasks when working on small projects. Users can collect tasks into categories like "Done", "In Progress" or "To Do" and SoloP will generate a markdown file laying them out in a user-friendly way.
 
Current Version: Version 1.0.0

## Example

Using SoloP will help you automatically manage a `SOLOP.md` file:

SOLOP.md:
```md
# PROJECT NAME

## BACKLOG

- [1]: Task to do

## IN PROGRESS

- [2]: Task currently in progress

## DONE

- [3]: Task completed
```

## Using SoloP

As of Version 1 *SoloP* is only accessible by the CLI. Tasks can be added, deleted and managed by executing `solop` from the command line.

### Actions

Calling `solop` with no flags will update the `SOLOP.md` file with any unsaved changes.

Note: Including the `--xmake` flag in any action will not publish the action to the `SOLOP.md` file, but the action will be visible next time the file is made.

| Action | Flag | Description |
| -------| ---- | ----------- |
| Add Task | `--add [Description]` | Adds a task to the Backlog with [Description]. Tasks are added with a `priority` of 1 by default. |
| Delete Task | `--delete [Task ID(s)]` | Deletes the specified tasks |
| Change Status | `--status [Status] [Task ID(s)]` | Moves the specified tasks into the [Status] section |
| Nest Task | `--nest [Child] [Parent]` | Nests [Child] task under the [Parent] task. Note: If the tasks are of different statuses, they will appear un-nested in their respective sections. Nesting will occur again when both tasks are re-united. |
| Un-nest Task | `--xchild [Child]` | Un-nests the [Child] task from all parents. Include the `--inherit` flag to move all [Child]'s children to any parents. When not included all children tasks follow [Child] |
| Change Priority | `--priority [Priority] [Task ID(s)]` | Changes the priority of the given tasks. All tasks are sorted in their respective sections/nests by priority. |

## Future Features

Future features will include: 

- Wrapping tasks up into versions
- Customisation options for sorting/visibility and more
- An interactive CLI for easier use
- Integration with git commits, to automatically update the file when features are committed to git
- Warnings and recommendations for too many bottlenecks, next tasks, etc...
- Pulling from SOLOP.md files for sharing and direct manipulation
- Development metrics to measure tasks done per session, etc...
- Managing of dependencies among tasks, automatically organising which tasks are more critical
- Automatic creation of a Change Log from git actions
- Milestones, feature wishlists and progress markers
