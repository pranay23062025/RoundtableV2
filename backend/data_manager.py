import pandas as pd
import streamlit as st
import os
from typing import Dict, List, Optional

class StudentDataManager:
    """Backend manager for student data operations"""
    
    def __init__(self, csv_path: str = "data/students.csv"):
        self.csv_path = csv_path
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Ensure the data directory exists"""
        data_dir = os.path.dirname(self.csv_path)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    @st.cache_data
    def load_students_data(_self) -> pd.DataFrame:
        """Load student data from CSV with caching"""
        try:
            if os.path.exists(_self.csv_path):
                df = pd.read_csv(_self.csv_path)
                return df
            else:
                # Create sample data if CSV doesn't exist
                return _self._create_sample_data()
        except Exception as e:
            st.error(f"Error loading student data: {str(e)}")
            return _self._create_sample_data()
    
    def _create_sample_data(self) -> pd.DataFrame:
        """Create sample student data if CSV doesn't exist"""
        sample_data = {
            'gvc_id': ['GVC001', 'GVC002', 'GVC003', 'GVC004', 'GVC005'],
            'name': ['Alex Johnson', 'Maya Patel', 'Sam Chen', 'Jordan Smith', 'Riley Davis'],
            'age': [16, 15, 17, 16, 15],
            'grade_level': ['Grade 10', 'Grade 9', 'Grade 11', 'Grade 10', 'Grade 9'],
            'email': ['alex.j@school.edu', 'maya.p@school.edu', 'sam.c@school.edu', 'jordan.s@school.edu', 'riley.d@school.edu'],
            'interests': [
                'computer programming, robotics, game design',
                'environmental science, biology, sustainability',
                'music production, digital art, creative writing',
                'sports medicine, fitness, nutrition',
                'psychology, social work, community service'
            ],
            'goals': [
                'Become a software engineer and develop innovative apps that help people solve everyday problems',
                'Study environmental engineering to help combat climate change and protect natural ecosystems',
                'Pursue a career in multimedia arts and create content that inspires and entertains others',
                'Become a physical therapist and help athletes recover from injuries while promoting healthy lifestyles',
                'Study psychology to become a counselor and help young people navigate mental health challenges'
            ],
            'strengths': [
                'logical thinking, problem-solving, attention to detail',
                'research skills, analytical thinking, environmental awareness',
                'creativity, artistic vision, storytelling ability',
                'empathy, physical fitness, leadership skills',
                'active listening, emotional intelligence, communication'
            ],
            'challenges': [
                'time management, public speaking, perfectionism',
                'math anxiety, test-taking stress, confidence in presentations',
                'self-discipline, financial planning, technical skills',
                'study habits, procrastination, balancing activities',
                'academic writing, organization, technology skills'
            ],
            'additional_info': [
                'Participates in coding club and volunteers at local library teaching seniors computer skills',
                'Member of environmental club, has organized several campus clean-up events',
                'Plays in school band, has won several art competitions, runs social media for drama club',
                'Team captain for soccer, volunteers at youth sports camps during summers',
                'Peer tutor, active in student government, volunteers at crisis helpline'
            ]
        }
        
        df = pd.DataFrame(sample_data)
        
        # Save sample data to CSV
        try:
            df.to_csv(self.csv_path, index=False)
            st.info(f"Created sample student data at {self.csv_path}")
        except Exception as e:
            st.warning(f"Could not save sample data: {str(e)}")
        
        return df
    
    def get_all_gvc_ids(self) -> List[str]:
        """Get list of all GVC IDs"""
        df = self.load_students_data()
        return sorted(df['gvc_id'].tolist())
    
    def get_student_by_gvc_id(self, gvc_id: str) -> Optional[Dict]:
        """Get student data by GVC ID"""
        df = self.load_students_data()
        student_row = df[df['gvc_id'] == gvc_id]
        
        if student_row.empty:
            return None
        
        # Convert to dictionary and clean up data
        student_data = student_row.iloc[0].to_dict()
        
        # Handle NaN values
        for key, value in student_data.items():
            if pd.isna(value):
                student_data[key] = ''
        
        return student_data
    
    def get_students_summary(self) -> Dict:
        """Get summary statistics about all students"""
        df = self.load_students_data()
        
        return {
            'total_students': len(df),
            'avg_age': df['age'].mean() if 'age' in df.columns else 0,
            'grade_distribution': df['grade_level'].value_counts().to_dict() if 'grade_level' in df.columns else {},
            'recent_students': df.head(5)['name'].tolist() if 'name' in df.columns else []
        }
    
    def search_students(self, query: str) -> pd.DataFrame:
        """Search students by name or GVC ID"""
        df = self.load_students_data()
        
        if not query:
            return df
        
        # Search in name and gvc_id columns
        mask = (
            df['name'].str.contains(query, case=False, na=False) |
            df['gvc_id'].str.contains(query, case=False, na=False)
        )
        
        return df[mask]
    
    def validate_student_data(self, data: Dict) -> List[str]:
        """Validate student data and return list of errors"""
        errors = []
        
        required_fields = ['gvc_id', 'name', 'age', 'grade_level']
        
        for field in required_fields:
            if not data.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Validate age
        if data.get('age'):
            try:
                age = int(data['age'])
                if age < 5 or age > 25:
                    errors.append("Age must be between 5 and 25")
            except ValueError:
                errors.append("Age must be a valid number")
        
        # Validate GVC ID format
        if data.get('gvc_id'):
            gvc_id = data['gvc_id']
            if not gvc_id.startswith('GVC') or len(gvc_id) != 6:
                errors.append("GVC ID must be in format 'GVC###' (e.g., GVC001)")
        
        return errors
    
    def add_student(self, student_data: Dict) -> bool:
        """Add a new student to the CSV"""
        try:
            # Validate data
            errors = self.validate_student_data(student_data)
            if errors:
                st.error(f"Validation errors: {', '.join(errors)}")
                return False
            
            # Load existing data
            df = self.load_students_data()
            
            # Check if GVC ID already exists
            if student_data['gvc_id'] in df['gvc_id'].values:
                st.error(f"Student with GVC ID {student_data['gvc_id']} already exists")
                return False
            
            # Add new student
            new_row = pd.DataFrame([student_data])
            df = pd.concat([df, new_row], ignore_index=True)
            
            # Save to CSV
            df.to_csv(self.csv_path, index=False)
            
            # Clear cache to reload data
            self.load_students_data.clear()
            
            st.success(f"Student {student_data['name']} added successfully!")
            return True
            
        except Exception as e:
            st.error(f"Error adding student: {str(e)}")
            return False
    
    def update_student(self, gvc_id: str, updated_data: Dict) -> bool:
        """Update an existing student's data"""
        try:
            df = self.load_students_data()
            
            # Find student
            student_index = df[df['gvc_id'] == gvc_id].index
            if student_index.empty:
                st.error(f"Student with GVC ID {gvc_id} not found")
                return False
            
            # Update data
            for key, value in updated_data.items():
                if key in df.columns:
                    df.loc[student_index[0], key] = value
            
            # Save to CSV
            df.to_csv(self.csv_path, index=False)
            
            # Clear cache
            self.load_students_data.clear()
            
            st.success(f"Student data updated successfully!")
            return True
            
        except Exception as e:
            st.error(f"Error updating student: {str(e)}")
            return False

# Global instance
data_manager = StudentDataManager()
