# Bibliography Manager

A real-time LaTeX bibliography management tool that automatically organizes and updates your references.

## Features

- Real-time monitoring of .tex file citation changes
- Automatic .bib file organization
- Citation context tracking
- Citation statistics
- Maintains citation order
- Multiple citation commands support

## Prerequisites

- Python 3.x

### Required packages:

- `bibtexparser`
- `watchdog`

## Output Format

The program organizes `references.bib` into:

### Header Information

- Last update time
- Reference counts
- File statistics

### Cited References Section

- Sorted by first appearance
- Citation frequency
- Context information
- Line numbers

### Uncited References Section

- Preserved for future use
- Original entry format

## Usage

### Processing Files in the Current Directory

To process files in the current directory, use:

```bash
bibmanager
```

### Watch Mode

To enable watch mode, which automatically updates the bibliography as changes occur, use:

```bash
bibmanager -w
```

### Specify Directory

To specify a directory for managing LaTeX projects, use:

```bash
bibmanager -d /path/to/latex/project
```

## Future Plans

### Short Term

- DOI lookup and metadata completion
- PDF file management
- Reference format validation

## Common Issues

### Python Not Found

- Ensure Python is installed and in PATH
- Restart terminal after installation

### Package Installation Fails

- Try running with administrator privileges
- Check internet connection
- Update pip: `python -m pip install --upgrade pip`

### File Encoding Issues

- Ensure .tex files are UTF-8 encoded
- Check for special characters

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Submit a pull request

## Support

For support:

- Open an issue
- Provide error messages
- Include minimal example

## License

This software is protected by copyright law. All rights reserved.

No part of this software may be reproduced, modified, distributed, or republished without prior written permission from the author.

Commercial use and redistribution are strictly prohibited.

Made with ❤️ for LaTeX users
