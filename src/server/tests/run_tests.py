#!/usr/bin/env python3
import pytest
import sys
import os
import argparse
import logging
from typing import List

def setup_logging():
    """Configure logging for test runner"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='MCP Server Test Runner')
    
    parser.add_argument(
        '--unit',
        action='store_true',
        help='Run unit tests only'
    )
    parser.add_argument(
        '--integration',
        action='store_true',
        help='Run integration tests'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Run all tests'
    )
    parser.add_argument(
        '--coverage',
        action='store_true',
        help='Generate coverage report'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose output'
    )
    parser.add_argument(
        '--deepseek',
        action='store_true',
        help='Run tests with Deepseek API integration'
    )
    
    return parser.parse_args()

def get_test_files() -> List[str]:
    """Get all test files in the tests directory"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_files = [
        os.path.join(current_dir, f) for f in [
            'test_injection_handler.py',
            'test_integration_manager.py',
            'test_mcp_server.py',
            'test_payload_manager.py',
            'test_waf_bypass.py',
            'test_api_routes.py'
        ]
    ]
    return test_files

def run_tests(args: argparse.Namespace) -> int:
    """Run tests with specified configuration"""
    logger = logging.getLogger(__name__)
    
    # Prepare pytest arguments
    pytest_args = []
    
    # Add verbosity
    if args.verbose:
        pytest_args.append('-v')
    
    # Add coverage options
    if args.coverage:
        pytest_args.extend([
            '--cov=src/server',
            '--cov-report=term-missing',
            '--cov-report=html'
        ])
    
    # Configure test selection
    if args.unit:
        pytest_args.extend([
            '-m', 'not integration',
            '--asyncio-mode=auto',  # Handle async tests
            '--tb=short',          # Shorter traceback format
            '--color=yes'          # Colored output
        ])
    elif args.integration:
        pytest_args.extend([
            '-m', 'integration',
            '--asyncio-mode=auto',
            '--tb=short',
            '--color=yes'
        ])
    
    # Add Deepseek API configuration if specified
    if args.deepseek:
        os.environ['DEEPSEEK_API_KEY'] = 'sk-1bd5de3f31db429cb8cbe73875537c5c'
        os.environ['DEEPSEEK_API_URL'] = 'https://api.deepseek.com/v1'
    
    # Add test files
    pytest_args.extend(get_test_files())
    
    # Run tests
    logger.info("Running tests with arguments: %s", ' '.join(pytest_args))
    return pytest.main(pytest_args)

def main():
    """Main entry point for test runner"""
    logger = setup_logging()
    args = parse_arguments()
    
    try:
        # Validate arguments
        if not any([args.unit, args.integration, args.all]):
            logger.error("Please specify test type: --unit, --integration, or --all")
            return 1
        
        # Run tests
        result = run_tests(args)
        
        # Handle results
        if result == 0:
            logger.info("All tests passed successfully!")
        else:
            logger.error("Some tests failed. Please check the output above.")
        
        return result
        
    except Exception as e:
        logger.error("Error running tests: %s", str(e))
        return 1

if __name__ == '__main__':
    sys.exit(main())
