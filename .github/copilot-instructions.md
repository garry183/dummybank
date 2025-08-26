# dummybank

dummybank is currently a minimal repository containing only basic documentation. This repository serves as a foundation for a banking application that will be built using modern web technologies.

**ALWAYS reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Current Repository State

This is a minimal repository with:
- Basic README.md containing just the project name
- No build system, dependencies, or source code yet
- No CI/CD pipelines configured
- Clean git history with minimal commits

**DO NOT attempt to build or run the application yet - there is no buildable code in the repository.**

## Working Effectively

### Initial Repository Setup
- Repository root: `/home/runner/work/dummybank/dummybank`
- Always use absolute paths when referring to repository files
- Verify repository location: `pwd` (should show the absolute path above)
- Check repository status: `git --no-pager status`
- List repository contents: `ls -la`

### Available Development Tools
The development environment includes the following validated tools:
- **Git**: `/usr/bin/git` (version 2.51.0)
- **Node.js**: `/usr/local/bin/node` (version v20.19.4)  
- **npm**: `/usr/local/bin/npm`
- **Python**: `/usr/bin/python3` (version 3.12.3)
- **pip**: `/usr/bin/pip`
- **Java**: `/usr/bin/java`
- **Maven**: `/usr/bin/mvn`
- **.NET**: `/usr/bin/dotnet`
- **Make**: `/usr/bin/make`
- **GCC**: `/usr/bin/gcc`

### Commands That Work Now
✅ **Validated working commands:**
- `pwd` - Show current directory
- `ls -la` - List all files including hidden ones
- `git --no-pager status` - Check git repository status
- `git --no-pager log --oneline -10` - Show recent commits
- `git --no-pager branch -a` - Show all branches
- `find . -name "*.md"` - Find markdown files
- `cat README.md` - Read README file

### Commands That Don't Work Yet
❌ **Commands that will fail (no build system yet):**
- `npm install` - No package.json exists
- `npm run build` - No package.json or build scripts
- `npm run test` - No test framework configured
- `make` - No Makefile exists
- `mvn install` - No Maven project structure
- `dotnet build` - No .NET project files
- Any build or test commands - No source code to build

## Future Development Framework

### When Code is Added to Repository

**CRITICAL BUILD TIMING WARNINGS:**
- **NEVER CANCEL build commands** - Allow full completion even if they take 45+ minutes
- **Set explicit timeouts of 60+ minutes** for any build commands when they are implemented
- **Set explicit timeouts of 30+ minutes** for test commands when they are implemented
- **Wait for completion** - Build and test processes may appear to hang but are often still working

### Expected Development Patterns

When this repository evolves into a full banking application, expect these patterns:

**For Node.js/JavaScript projects:**
- Install dependencies: `npm install` (Set timeout: 300+ seconds)
- Build application: `npm run build` (NEVER CANCEL - Set timeout: 3600+ seconds)
- Run tests: `npm run test` (NEVER CANCEL - Set timeout: 1800+ seconds)  
- Start development server: `npm run dev`
- Lint code: `npm run lint` (always run before commits)
- Format code: `npm run format` (always run before commits)

**For Java/Maven projects:**
- Install dependencies: `mvn install` (NEVER CANCEL - Set timeout: 3600+ seconds)
- Build project: `mvn compile` (NEVER CANCEL - Set timeout: 3600+ seconds)
- Run tests: `mvn test` (NEVER CANCEL - Set timeout: 1800+ seconds)
- Package application: `mvn package` (NEVER CANCEL - Set timeout: 3600+ seconds)

**For .NET projects:**
- Restore packages: `dotnet restore` (Set timeout: 300+ seconds)
- Build project: `dotnet build` (NEVER CANCEL - Set timeout: 3600+ seconds)
- Run tests: `dotnet test` (NEVER CANCEL - Set timeout: 1800+ seconds)
- Run application: `dotnet run`

**For Python projects:**
- Install dependencies: `pip install -r requirements.txt` (Set timeout: 300+ seconds)
- Run tests: `python -m pytest` (NEVER CANCEL - Set timeout: 1800+ seconds)
- Lint code: `flake8` or `pylint` (always run before commits)

## Validation Requirements

### Manual Validation Steps
When code is implemented, **ALWAYS** perform these validation steps after making changes:

1. **Build Validation**: Ensure the application builds successfully
2. **Test Validation**: Run the full test suite and verify all tests pass
3. **Functional Validation**: Exercise key user scenarios manually
4. **Lint Validation**: Run all linters and code formatters

### Future Application Validation Scenarios
When the banking application is implemented, test these scenarios:

**Core Banking Operations:**
- User account creation and authentication
- Account balance inquiries  
- Money transfers between accounts
- Transaction history viewing
- Account statement generation

**Security Validation:**
- Authentication flows work correctly
- Authorization checks prevent unauthorized access
- Input validation prevents injection attacks
- Session management functions properly

**Performance Validation:**
- Application starts up within reasonable time
- Database operations complete efficiently  
- User interface responds promptly to interactions

## Repository Structure (Current)

```
/home/runner/work/dummybank/dummybank/
├── .git/                   # Git repository metadata
├── .github/               # GitHub configuration (created for Copilot instructions)
│   └── copilot-instructions.md  # This file
└── README.md              # Basic project documentation
```

**Current file listing output:**
```bash
$ find . -type f | grep -v ".git" | sort
./.github/copilot-instructions.md
./README.md
```

## Common Commands Reference

### Repository Management
- **Check repository status**: `git --no-pager status`
- **View recent changes**: `git --no-pager diff`
- **View recent commits**: `git --no-pager log --oneline -10`
- **List all files**: `find . -type f | grep -v ".git" | sort`

### Environment Information
- **Current directory**: `pwd`
- **Available disk space**: `df -h .`
- **System information**: `uname -a`
- **Development tools**: `which git node npm python3 java mvn dotnet make gcc`

## Key Reminders

1. **ALWAYS follow these instructions first** - Only search or explore when information here is incomplete or incorrect
2. **NEVER CANCEL long-running commands** - Builds and tests may take 45+ minutes
3. **Use explicit timeouts** - Set 60+ minutes for builds, 30+ minutes for tests
4. **Validate everything manually** - Test real user scenarios after making changes
5. **Run linters before commits** - Prevent CI failures by running code quality checks
6. **Document command timing** - Note actual execution times for future reference
7. **Use absolute paths** - Always reference files with full paths starting from `/home/runner/work/dummybank/dummybank`

## Getting Started Checklist

When beginning work on this repository:
- [ ] Verify you're in the correct directory: `/home/runner/work/dummybank/dummybank`
- [ ] Check git status: `git --no-pager status`  
- [ ] Review current repository contents: `ls -la`
- [ ] Read the README.md: `cat README.md`
- [ ] Understand this is a minimal repository with no buildable code yet
- [ ] Plan development approach based on intended technology stack
- [ ] When adding code, follow the build/test patterns outlined above
- [ ] Always validate changes manually before completing work