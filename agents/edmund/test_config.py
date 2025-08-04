#!/usr/bin/env python3
"""
Configuration validation and testing for Edmund
Tests all configuration files for syntax, completeness, and consistency
"""

import json
import yaml
import os
import sys
from typing import Dict, List, Any, Tuple

class EdmundConfigTester:
    def __init__(self):
        self.base_path = os.path.dirname(__file__)
        self.errors = []
        self.warnings = []
        
    def log_error(self, message: str):
        """Log an error message"""
        self.errors.append(f"❌ ERROR: {message}")
        print(f"❌ ERROR: {message}")
        
    def log_warning(self, message: str):
        """Log a warning message"""
        self.warnings.append(f"⚠️ WARNING: {message}")
        print(f"⚠️ WARNING: {message}")
        
    def log_success(self, message: str):
        """Log a success message"""
        print(f"✅ {message}")
        
    def load_json_file(self, filename: str) -> Tuple[Dict[str, Any], bool]:
        """Load and validate JSON file"""
        filepath = os.path.join(self.base_path, filename)
        
        if not os.path.exists(filepath):
            self.log_error(f"File not found: {filename}")
            return {}, False
            
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            self.log_success(f"Valid JSON: {filename}")
            return data, True
        except json.JSONDecodeError as e:
            self.log_error(f"Invalid JSON in {filename}: {str(e)}")
            return {}, False
        except Exception as e:
            self.log_error(f"Error reading {filename}: {str(e)}")
            return {}, False
            
    def load_yaml_file(self, filename: str) -> Tuple[Dict[str, Any], bool]:
        """Load and validate YAML file"""
        filepath = os.path.join(self.base_path, filename)
        
        if not os.path.exists(filepath):
            self.log_error(f"File not found: {filename}")
            return {}, False
            
        try:
            with open(filepath, 'r') as f:
                data = yaml.safe_load(f)
            self.log_success(f"Valid YAML: {filename}")
            return data, True
        except yaml.YAMLError as e:
            self.log_error(f"Invalid YAML in {filename}: {str(e)}")
            return {}, False
        except Exception as e:
            self.log_error(f"Error reading {filename}: {str(e)}")
            return {}, False
            
    def test_agent_config(self) -> bool:
        """Test agent-config.json"""
        print("\n🧪 Testing agent-config.json")
        print("-" * 40)
        
        config, valid = self.load_json_file('agent-config.json')
        if not valid:
            return False
            
        # Test required fields
        required_fields = [
            'agent', 'model', 'instructions', 'knowledgeSources', 
            'tools', 'features', 'security', 'deployment'
        ]
        
        for field in required_fields:
            if field not in config:
                self.log_error(f"Missing required field: {field}")
                valid = False
            else:
                self.log_success(f"Required field present: {field}")
                
        # Test agent section
        if 'agent' in config:
            agent = config['agent']
            if agent.get('name') != 'Edmund':
                self.log_warning(f"Agent name is '{agent.get('name')}', expected 'Edmund'")
            if 'displayName' not in agent:
                self.log_error("Missing agent.displayName")
                
        # Test model configuration
        if 'model' in config:
            model = config['model']
            if model.get('modelName') != 'gpt-4-turbo':
                self.log_warning(f"Model is '{model.get('modelName')}', expected 'gpt-4-turbo'")
            if model.get('temperature') is None:
                self.log_error("Missing model.temperature")
                
        # Test knowledge sources
        if 'knowledgeSources' in config:
            sources = config['knowledgeSources']
            if not isinstance(sources, list) or len(sources) == 0:
                self.log_error("knowledgeSources should be a non-empty list")
            else:
                github_source_found = False
                for source in sources:
                    if 'github.com/bengweeks/T-Minus-15' in source.get('url', ''):
                        github_source_found = True
                        break
                if not github_source_found:
                    self.log_warning("T-Minus-15 GitHub repository not found in knowledge sources")
                    
        return valid
        
    def test_knowledge_sources(self) -> bool:
        """Test knowledge-sources.json"""
        print("\n🧪 Testing knowledge-sources.json")
        print("-" * 40)
        
        config, valid = self.load_json_file('knowledge-sources.json')
        if not valid:
            return False
            
        # Test structure
        if 'knowledgeSources' not in config:
            self.log_error("Missing 'knowledgeSources' root key")
            return False
            
        sources = config['knowledgeSources']
        if not isinstance(sources, list):
            self.log_error("knowledgeSources should be a list")
            return False
            
        # Test each source
        tminus15_found = False
        for i, source in enumerate(sources):
            if 'id' not in source:
                self.log_error(f"Source {i}: Missing 'id' field")
                valid = False
            if 'source' not in source:
                self.log_error(f"Source {i}: Missing 'source' field")
                valid = False
            elif 'url' in source['source']:
                if 'T-Minus-15' in source['source']['url']:
                    tminus15_found = True
                    
        if not tminus15_found:
            self.log_error("T-Minus-15 repository not found in knowledge sources")
            valid = False
        else:
            self.log_success("T-Minus-15 repository found in knowledge sources")
            
        return valid
        
    def test_deployment_config(self) -> bool:
        """Test deployment.yaml"""
        print("\n🧪 Testing deployment.yaml")
        print("-" * 40)
        
        filepath = os.path.join(self.base_path, 'deployment.yaml')
        
        if not os.path.exists(filepath):
            self.log_error("File not found: deployment.yaml")
            return False
            
        try:
            with open(filepath, 'r') as f:
                # Load all YAML documents
                docs = list(yaml.safe_load_all(f))
            self.log_success(f"Valid YAML: deployment.yaml ({len(docs)} documents)")
            
            valid = True
            # Test first document (main agent config)
            if len(docs) > 0:
                config = docs[0]
                if 'apiVersion' not in config:
                    self.log_error("Missing apiVersion in first document")
                    valid = False
                if 'kind' not in config:
                    self.log_error("Missing kind in first document")
                    valid = False
                elif config['kind'] != 'Agent':
                    self.log_warning(f"Kind is '{config['kind']}', expected 'Agent'")
                    
                if 'metadata' not in config:
                    self.log_error("Missing metadata section")
                    valid = False
                elif 'name' not in config['metadata']:
                    self.log_error("Missing metadata.name")
                    valid = False
                    
                if 'spec' not in config:
                    self.log_error("Missing spec section")
                    valid = False
            else:
                self.log_error("No YAML documents found")
                valid = False
                
            return valid
            
        except yaml.YAMLError as e:
            self.log_error(f"Invalid YAML in deployment.yaml: {str(e)}")
            return False
        except Exception as e:
            self.log_error(f"Error reading deployment.yaml: {str(e)}")
            return False
        
    def test_mcp_config(self) -> bool:
        """Test mcp-config.json"""
        print("\n🧪 Testing mcp-config.json")
        print("-" * 40)
        
        config, valid = self.load_json_file('mcp-config.json')
        if not valid:
            return False
            
        # Test structure
        required_sections = ['mcpConfiguration', 'servers', 'security', 'monitoring']
        for section in required_sections:
            if section not in config:
                self.log_error(f"Missing section: {section}")
                valid = False
            else:
                self.log_success(f"Section present: {section}")
                
        # Test servers configuration
        if 'servers' in config:
            servers = config['servers']
            if not isinstance(servers, list):
                self.log_error("servers should be a list")
                valid = False
            else:
                expected_servers = ['azure-devops-connector', 'github-connector']
                found_servers = [s.get('id') for s in servers]
                for expected in expected_servers:
                    if expected in found_servers:
                        self.log_success(f"MCP server configured: {expected}")
                    else:
                        self.log_warning(f"MCP server not found: {expected}")
                        
        return valid
        
    def test_requirements(self) -> bool:
        """Test requirements.txt"""
        print("\n🧪 Testing requirements.txt")
        print("-" * 40)
        
        filepath = os.path.join(self.base_path, 'requirements.txt')
        if not os.path.exists(filepath):
            self.log_error("requirements.txt not found")
            return False
            
        try:
            with open(filepath, 'r') as f:
                content = f.read()
                
            # Check for essential dependencies
            essential_deps = [
                'azure-ai-foundry',
                'openai',
                'langchain',
                'fastapi',
                'pydantic'
            ]
            
            valid = True
            for dep in essential_deps:
                if dep in content:
                    self.log_success(f"Essential dependency found: {dep}")
                else:
                    self.log_warning(f"Essential dependency missing: {dep}")
                    
            return valid
            
        except Exception as e:
            self.log_error(f"Error reading requirements.txt: {str(e)}")
            return False
            
    def test_markdown_config(self) -> bool:
        """Test edmund.md"""
        print("\n🧪 Testing edmund.md")
        print("-" * 40)
        
        filepath = os.path.join(self.base_path, 'edmund.md')
        if not os.path.exists(filepath):
            self.log_error("edmund.md not found")
            return False
            
        try:
            with open(filepath, 'r') as f:
                content = f.read()
                
            # Check for essential sections
            essential_sections = [
                '# Edmund (the Engineer)',
                '## Introduction',
                '## Role & Responsibilities', 
                '## T-Minus-15 Engineering Expertise',
                '## Example Tasks',
                '## Communication Style & Tone',
                '## Values & Alignment'
            ]
            
            valid = True
            for section in essential_sections:
                if section in content:
                    self.log_success(f"Section found: {section}")
                else:
                    self.log_error(f"Missing section: {section}")
                    valid = False
                    
            # Check for T-Minus-15 references
            tminus15_refs = ['T-Minus-15', '15-step', 'DevOps', 'methodology']
            found_refs = sum(1 for ref in tminus15_refs if ref in content)
            
            if found_refs >= 3:
                self.log_success(f"Good T-Minus-15 methodology coverage ({found_refs} references)")
            else:
                self.log_warning(f"Limited T-Minus-15 methodology coverage ({found_refs} references)")
                
            return valid
            
        except Exception as e:
            self.log_error(f"Error reading edmund.md: {str(e)}")
            return False
            
    def test_file_permissions(self) -> bool:
        """Test file permissions and structure"""
        print("\n🧪 Testing file permissions and structure")
        print("-" * 40)
        
        required_files = [
            'edmund.md',
            'agent-config.json',
            'knowledge-sources.json',
            'deployment.yaml',
            'requirements.txt',
            'mcp-config.json',
            'README.md'
        ]
        
        valid = True
        for filename in required_files:
            filepath = os.path.join(self.base_path, filename)
            if os.path.exists(filepath):
                if os.access(filepath, os.R_OK):
                    self.log_success(f"File readable: {filename}")
                else:
                    self.log_error(f"File not readable: {filename}")
                    valid = False
            else:
                self.log_error(f"File missing: {filename}")
                valid = False
                
        return valid
        
    def run_all_tests(self) -> bool:
        """Run all configuration tests"""
        print("🧪 EDMUND CONFIGURATION TESTING SUITE")
        print("=" * 60)
        
        all_valid = True
        
        # Run individual tests
        tests = [
            self.test_file_permissions,
            self.test_markdown_config,
            self.test_agent_config,
            self.test_knowledge_sources,
            self.test_deployment_config,
            self.test_mcp_config,
            self.test_requirements
        ]
        
        for test in tests:
            if not test():
                all_valid = False
                
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        if all_valid:
            print("✅ ALL TESTS PASSED!")
            print("Edmund's configuration is ready for deployment.")
        else:
            print("❌ SOME TESTS FAILED!")
            print(f"Errors: {len(self.errors)}")
            print(f"Warnings: {len(self.warnings)}")
            
        if self.errors:
            print("\n🚨 ERRORS TO FIX:")
            for error in self.errors:
                print(f"  {error}")
                
        if self.warnings:
            print("\n⚠️ WARNINGS TO CONSIDER:")
            for warning in self.warnings:
                print(f"  {warning}")
                
        return all_valid

def main():
    """Main function"""
    tester = EdmundConfigTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()