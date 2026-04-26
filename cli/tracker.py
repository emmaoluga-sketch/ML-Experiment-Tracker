#!/usr/bin/env python
"""CLI for ML Experiment Tracker."""

import argparse
import json
import sys
import os
from typing import Dict, Any, List
import requests
from tabulate import tabulate
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_URL = os.getenv("TRACKER_API_URL", "http://127.0.0.1:8000")
BASE_URL = f"{API_URL}/experiments"


class TrackerClient:
    """Client for interacting with ML Experiment Tracker API."""
    
    def __init__(self, api_url: str = BASE_URL):
        self.api_url = api_url
    
    def create_experiment(
        self,
        name: str,
        params: Dict[str, Any] = None,
        metrics: Dict[str, Any] = None,
        tags: List[str] = None,
        description: str = None,
        notes: str = None
    ) -> Dict:
        """Create a new experiment."""
        payload = {
            "name": name,
            "params": params or {},
            "metrics": metrics or {},
            "tags": tags or [],
            "description": description,
            "notes": notes
        }
        
        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            result = response.json()
            print(f"✓ Experiment created successfully")
            print(f"  ID: {result['id']}")
            print(f"  Name: {result['name']}")
            print(f"  Created: {result['created_at']}")
            return result
        except requests.exceptions.RequestException as e:
            print(f"✗ Error creating experiment: {str(e)}")
            sys.exit(1)
    
    def list_experiments(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """List all experiments."""
        try:
            response = requests.get(self.api_url, params={"skip": skip, "limit": limit})
            response.raise_for_status()
            experiments = response.json()
            
            if not experiments:
                print("No experiments found")
                return experiments
            
            # Prepare table data
            table_data = []
            for exp in experiments:
                table_data.append([
                    exp['id'],
                    exp['name'],
                    exp['created_at'][:10],  # Date only
                    len(exp.get('tags', []) or []),
                    len(exp.get('metrics', {}) or {})
                ])
            
            headers = ["ID", "Name", "Created", "Tags", "Metrics"]
            print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))
            print(f"\nTotal: {len(experiments)} experiment(s)\n")
            
            return experiments
        except requests.exceptions.RequestException as e:
            print(f"✗ Error listing experiments: {str(e)}")
            sys.exit(1)
    
    def get_experiment(self, experiment_id: int) -> Dict:
        """Get experiment details."""
        try:
            response = requests.get(f"{self.api_url}/{experiment_id}")
            response.raise_for_status()
            exp = response.json()
            
            print(f"\n{'='*60}")
            print(f"Experiment: {exp['name']} (ID: {exp['id']})")
            print(f"{'='*60}")
            print(f"Description: {exp.get('description', 'N/A')}")
            print(f"Created: {exp['created_at']}")
            print(f"Updated: {exp['updated_at']}")
            print(f"Tags: {', '.join(exp.get('tags', []) or [])}")
            
            if exp.get('params'):
                print(f"\nParameters:")
                for key, value in exp['params'].items():
                    print(f"  {key}: {value}")
            
            if exp.get('metrics'):
                print(f"\nMetrics:")
                for key, value in exp['metrics'].items():
                    print(f"  {key}: {value}")
            
            if exp.get('notes'):
                print(f"\nNotes: {exp['notes']}")
            
            print(f"{'='*60}\n")
            
            return exp
        except requests.exceptions.RequestException as e:
            print(f"✗ Error getting experiment: {str(e)}")
            sys.exit(1)
    
    def delete_experiment(self, experiment_id: int) -> bool:
        """Delete an experiment."""
        try:
            response = requests.delete(f"{self.api_url}/{experiment_id}")
            response.raise_for_status()
            print(f"✓ Experiment {experiment_id} deleted successfully")
            return True
        except requests.exceptions.RequestException as e:
            print(f"✗ Error deleting experiment: {str(e)}")
            sys.exit(1)
    
    def update_experiment(
        self,
        experiment_id: int,
        **kwargs
    ) -> Dict:
        """Update an experiment."""
        try:
            response = requests.put(f"{self.api_url}/{experiment_id}", json=kwargs)
            response.raise_for_status()
            print(f"✓ Experiment {experiment_id} updated successfully")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"✗ Error updating experiment: {str(e)}")
            sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="ML Experiment Tracker CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s run --name "baseline" --params '{"lr": 0.1}' --metrics '{"acc": 0.85}'
  %(prog)s list
  %(prog)s detail --id 1
  %(prog)s delete --id 1
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Log a new experiment")
    run_parser.add_argument("--name", required=True, help="Experiment name")
    run_parser.add_argument("--params", default="{}", help="JSON parameters")
    run_parser.add_argument("--metrics", default="{}", help="JSON metrics")
    run_parser.add_argument("--tags", help="Comma-separated tags")
    run_parser.add_argument("--description", help="Experiment description")
    run_parser.add_argument("--notes", help="Additional notes")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all experiments")
    list_parser.add_argument("--limit", type=int, default=100, help="Max experiments to show")
    list_parser.add_argument("--skip", type=int, default=0, help="Skip first N experiments")
    
    # Detail command
    detail_parser = subparsers.add_parser("detail", help="Show experiment details")
    detail_parser.add_argument("--id", type=int, required=True, help="Experiment ID")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete an experiment")
    delete_parser.add_argument("--id", type=int, required=True, help="Experiment ID")
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update an experiment")
    update_parser.add_argument("--id", type=int, required=True, help="Experiment ID")
    update_parser.add_argument("--name", help="New experiment name")
    update_parser.add_argument("--metrics", help="Updated JSON metrics")
    update_parser.add_argument("--notes", help="Updated notes")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    client = TrackerClient()
    
    try:
        if args.command == "run":
            params = json.loads(args.params)
            metrics = json.loads(args.metrics)
            tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
            
            client.create_experiment(
                name=args.name,
                params=params,
                metrics=metrics,
                tags=tags,
                description=args.description,
                notes=args.notes
            )
        
        elif args.command == "list":
            client.list_experiments(skip=args.skip, limit=args.limit)
        
        elif args.command == "detail":
            client.get_experiment(args.id)
        
        elif args.command == "delete":
            client.delete_experiment(args.id)
        
        elif args.command == "update":
            update_data = {}
            if args.name:
                update_data['name'] = args.name
            if args.metrics:
                update_data['metrics'] = json.loads(args.metrics)
            if args.notes:
                update_data['notes'] = args.notes
            
            client.update_experiment(args.id, **update_data)
    
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
