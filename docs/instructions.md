# Instructions for Asset Management

## Overview

This document provides detailed instructions for managing ComfyUI model downloads and asset organization.

## Core Responsibilities

1. Download Management
2. Directory Organization
3. File Processing
4. Error Handling
5. Progress Tracking

## Detailed Instructions

### 1. Download Management

When processing download links:

- Verify link validity before downloading
- Implement retry logic for failed downloads
- Check for existing files before downloading
- Track download progress
- Log all download attempts

### 2. Directory Organization

For organizing downloaded assets:

- Create directories dynamically based on file types
- Follow the naming convention: lowercase with underscores
- Standard directories include:
  - models/
  - controlnets/
  - ip_adapters/
  - etc. (based on actual needs)

### 3. File Processing

For each downloaded file:

1. Verify file integrity
2. Rename if necessary following conventions
3. Move to appropriate directory
4. Update logs

### 4. Error Handling

When encountering issues:

1. Log error details
2. Attempt retry if appropriate
3. Report failures with context
4. Maintain error statistics

### 5. Progress Tracking

Maintain detailed logs of:

- Successful downloads
- Failed attempts
- Directory creation
- File movements
- Error occurrences

## Implementation Notes

- Use provided Python utilities in src/ directory
- Follow error handling procedures in error_handling.md
- Maintain consistent logging format

## Success Criteria

- All files downloaded successfully
- Proper directory organization
- Complete error logs
- Verified file integrity
- Updated tracking information