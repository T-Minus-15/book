#!/usr/bin/env python3
"""
Local testing script for Edmund the Engineer
Tests Edmund's personality, T-Minus-15 knowledge, and capabilities
"""

import os
import json
import requests
from openai import OpenAI
from typing import Dict, List, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class EdmundLocalTester:
    def __init__(self):
        """Initialize the local Edmund tester"""
        self.client = None
        self.config = self.load_edmund_config()
        self.setup_openai_client()
        
    def load_edmund_config(self) -> Dict[str, Any]:
        """Load Edmund's configuration from agent-config.json"""
        config_path = os.path.join(os.path.dirname(__file__), 'agent-config.json')
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def setup_openai_client(self):
        """Setup OpenAI client for local testing"""
        # You can use either OpenAI directly or Azure OpenAI
        api_key = os.getenv('OPENAI_API_KEY') or os.getenv('AZURE_OPENAI_API_KEY')
        base_url = os.getenv('AZURE_OPENAI_ENDPOINT')
        
        if not api_key:
            print("❌ Error: Please set OPENAI_API_KEY or AZURE_OPENAI_API_KEY environment variable")
            return
            
        if base_url:
            # Azure OpenAI
            self.client = OpenAI(
                api_key=api_key,
                base_url=f"{base_url.rstrip('/')}/openai/deployments/gpt-4o/",
                default_headers={"api-version": "2024-12-01-preview"}
            )
            print(f"✅ Using Azure OpenAI endpoint: {base_url}")
        else:
            # Regular OpenAI
            self.client = OpenAI(api_key=api_key)
            print("✅ Using OpenAI API")
    
    def get_edmund_system_prompt(self) -> str:
        """Get Edmund's system prompt from configuration"""
        base_prompt = self.config['instructions']['systemPrompt']
        
        # Add T-Minus-15 knowledge context
        tminus15_context = """
        
You have deep knowledge of the T-Minus-15 methodology from https://github.com/bengweeks/T-Minus-15, including:

T-Minus-15 Framework:
- 15-step process from idea to production
- 5-stage DevOps lifecycle: Prep > Design > Engineer > Test > Operate
- Cross-functional team structure with specialized roles
- Agile/Scrum practices with 2-3 week sprints
- Infrastructure-as-Code and automation focus
- Continuous integration and deployment practices

Your Role as Edmund the Engineer:
- Step 8: Design the Solution Architecture
- Step 9: Set Up the DevOps Pipeline & Tools  
- Step 10: Execute Iterative Development
- Step 11: Integrate Continuous Testing
- Step 12: Deploy Frequently and Operate

Team Values: Passionate, Creative, Free, Agile, Accountable, Knowledgeable, Transparent, Together, Doers, Strong

You work collaboratively with: Pepper (Prepper), Danny (Designer), Teddy (Tester), Ollie (Operator), Poppy (Planner)
        """
        
        return base_prompt + tminus15_context
    
    def test_edmund_response(self, prompt: str, test_name: str = "") -> str:
        """Test Edmund's response to a given prompt"""
        if not self.client:
            return "❌ OpenAI client not initialized"
            
        try:
            # Use the deployed model name directly (since we're using deployment-specific URL)
            model_names = ["gpt-4o"]
            
            for model_name in model_names:
                try:
                    response = self.client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": self.get_edmund_system_prompt()},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=self.config['model']['temperature'],
                        max_tokens=self.config['model']['maxTokens']
                    )
                    print(f"✅ Successfully connected using model: {model_name}")
                    break
                except Exception as e:
                    print(f"⚠️ Model '{model_name}' failed: {str(e)}")
                    if model_name == model_names[-1]:  # Last attempt
                        raise e
                    continue
            
            result = response.choices[0].message.content
            print(f"\n{'='*60}")
            print(f"🧪 TEST: {test_name}")
            print(f"{'='*60}")
            print(f"📝 Prompt: {prompt}")
            print(f"🤖 Edmund's Response:\n{result}")
            print(f"{'='*60}")
            
            return result
            
        except Exception as e:
            error_msg = f"❌ Error testing Edmund: {str(e)}"
            print(error_msg)
            return error_msg
    
    def run_personality_tests(self):
        """Test Edmund's personality and communication style"""
        print("\n🎭 TESTING EDMUND'S PERSONALITY")
        print("="*80)
        
        tests = [
            ("Hello Edmund, introduce yourself", "Personality Introduction"),
            ("What's your role in the T-Minus-15 team?", "Role Understanding"),
            ("How do you work with other team members?", "Collaboration Style"),
            ("What are your core values?", "Values Alignment")
        ]
        
        for prompt, test_name in tests:
            self.test_edmund_response(prompt, test_name)
    
    def run_tminus15_knowledge_tests(self):
        """Test Edmund's T-Minus-15 methodology knowledge"""
        print("\n📚 TESTING T-MINUS-15 KNOWLEDGE")
        print("="*80)
        
        tests = [
            ("Explain the T-Minus-15 methodology", "Methodology Overview"),
            ("What are the 15 steps from idea to production?", "15 Steps Knowledge"),
            ("Describe the 5-stage DevOps lifecycle", "DevOps Lifecycle"),
            ("What are your specific engineering responsibilities in T-Minus-15?", "Engineering Role"),
            ("How does T-Minus-15 integrate Agile and DevOps?", "Agile/DevOps Integration")
        ]
        
        for prompt, test_name in tests:
            self.test_edmund_response(prompt, test_name)
    
    def run_technical_capability_tests(self):
        """Test Edmund's technical capabilities"""
        print("\n⚙️ TESTING TECHNICAL CAPABILITIES")
        print("="*80)
        
        tests = [
            ("Help me set up a CI/CD pipeline for a Node.js application", "CI/CD Setup"),
            ("Review this Python code for best practices: def calc(x,y): return x+y", "Code Review"),
            ("Design a microservices architecture for an e-commerce platform", "Architecture Design"),
            ("How would you implement Infrastructure-as-Code for Azure?", "IaC Implementation"),
            ("What's your approach to automated testing in a DevOps pipeline?", "Testing Strategy")
        ]
        
        for prompt, test_name in tests:
            self.test_edmund_response(prompt, test_name)
    
    def run_problem_solving_tests(self):
        """Test Edmund's problem-solving capabilities"""
        print("\n🔧 TESTING PROBLEM-SOLVING CAPABILITIES")
        print("="*80)
        
        tests = [
            ("Our deployment pipeline is failing. How would you troubleshoot it?", "Troubleshooting"),
            ("The application is running slowly in production. What would you investigate?", "Performance Analysis"),
            ("We need to scale our system to handle 10x more traffic. What's your approach?", "Scaling Strategy"),
            ("Help me implement security best practices for our API", "Security Implementation")
        ]
        
        for prompt, test_name in tests:
            self.test_edmund_response(prompt, test_name)
    
    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🚀 STARTING EDMUND LOCAL TESTING SUITE")
        print("="*80)
        print(f"📋 Configuration: {self.config['agent']['name']}")
        print(f"🤖 Model: {self.config['model']['modelName']}")
        print(f"🌡️ Temperature: {self.config['model']['temperature']}")
        
        if not self.client:
            print("❌ Cannot run tests: OpenAI client not initialized")
            return
            
        # Run all test categories
        self.run_personality_tests()
        self.run_tminus15_knowledge_tests()  
        self.run_technical_capability_tests()
        self.run_problem_solving_tests()
        
        print("\n✅ EDMUND TESTING COMPLETE!")
        print("="*80)
        print("💡 Next steps:")
        print("1. Review Edmund's responses for accuracy and personality")
        print("2. Adjust configuration if needed")
        print("3. Deploy to Azure AI Foundry when satisfied")

def main():
    """Main testing function"""
    print("🧪 Edmund Local Testing Script")
    print("="*40)
    
    # Check environment variables
    if not (os.getenv('OPENAI_API_KEY') or os.getenv('AZURE_OPENAI_API_KEY')):
        print("\n❌ Missing API Key!")
        print("Please create a .env file with your API keys:")
        print("  1. Copy .env.example to .env")
        print("  2. Edit .env with your actual API keys")
        print("  3. Required variables:")
        print("     - AZURE_OPENAI_API_KEY=your-azure-key")
        print("     - AZURE_OPENAI_ENDPOINT=your-azure-endpoint")
        print("  4. Or use: OPENAI_API_KEY=your-openai-key")
        return
    
    # Initialize and run tests
    tester = EdmundLocalTester()
    
    # Interactive menu
    while True:
        print("\n📋 EDMUND TESTING MENU")
        print("="*30)
        print("1. Run all tests")
        print("2. Test personality only")
        print("3. Test T-Minus-15 knowledge only")
        print("4. Test technical capabilities only") 
        print("5. Test problem-solving only")
        print("6. Custom prompt test")
        print("7. Exit")
        
        choice = input("\nSelect option (1-7): ").strip()
        
        if choice == '1':
            tester.run_all_tests()
        elif choice == '2':
            tester.run_personality_tests()
        elif choice == '3':
            tester.run_tminus15_knowledge_tests()
        elif choice == '4':
            tester.run_technical_capability_tests()
        elif choice == '5':
            tester.run_problem_solving_tests()
        elif choice == '6':
            custom_prompt = input("Enter your custom prompt: ")
            tester.test_edmund_response(custom_prompt, "Custom Test")
        elif choice == '7':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Please select 1-7.")

if __name__ == "__main__":
    main()