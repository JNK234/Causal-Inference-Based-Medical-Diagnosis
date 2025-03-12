"""
Demo script showing how to use the chat interface.
"""
from App.chat.session import ChatSession

def main():
    # Initialize chat session
    session = ChatSession()
    
    print("Medical Case Analysis Chat Interface")
    print("===================================")
    print("\nEnter case details (type 'exit' to quit):")
    
    while True:
        # Get case details
        case_details = input("\nCase details: ")
        if case_details.lower() == 'exit':
            break
            
        # Process the case
        result = session.start_case(case_details)
        print("\nAnalysis Result:")
        print(result['response'])
        
        while True:
            # Get approval/improvement
            print("\nOptions:")
            print("1. Approve")
            print("2. Improve")
            print("3. Start New Case")
            choice = input("Choose option (1-3): ")
            
            if choice == '1':
                # Approve current stage
                result = session.approve_stage(approved=True)
                print("\nStage completed!")
                break
            elif choice == '2':
                # Get improvement text
                improvement = input("\nEnter improvements: ")
                result = session.approve_stage(approved=False, improvement_text=improvement)
                print("\nUpdated Analysis:")
                print(result['response'])
            elif choice == '3':
                # Clear session and start new case
                session.clear_session()
                break
            else:
                print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
