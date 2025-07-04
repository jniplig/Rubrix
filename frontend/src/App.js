import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Your API base URL (update this with your actual forwarded URL)
const API_BASE = '/api';

function App() {
  const [currentGroup, setCurrentGroup] = useState(null);
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [assessments, setAssessments] = useState({});

  // Load students for a specific group
  const loadGroup = async (group) => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE}/students/group/${group}`);
      setStudents(response.data.students);
      setCurrentGroup(group);
    } catch (error) {
      console.error('Error loading students:', error);
      alert('Error loading students. Check your connection.');
    }
    setLoading(false);
  };

  // Create an assessment
  const createAssessment = async (studentId, criterion, grade) => {
    try {
      const assessment = {
        student_id: studentId,
        criterion: criterion,
        grade: grade,
        notes: `Group ${currentGroup} assessment`
      };
      
      await axios.post(`${API_BASE}/assessments`, assessment);
      
      // Update local state
      setAssessments(prev => ({
        ...prev,
        [`${studentId}-${criterion}`]: grade
      }));
      
      alert('Assessment saved!');
    } catch (error) {
      console.error('Error saving assessment:', error);
      alert('Error saving assessment');
    }
  };

  const getGradeColor = (grade) => {
    const colors = {
      1: '#0ea5e9', // Teal - 1+
      2: '#3b82f6', // Blue - 1  
      3: '#eab308', // Yellow - 2
      4: '#f97316', // Orange - 3
      5: '#ef4444'  // Red - 4
    };
    return colors[grade] || '#e5e7eb';
  };

  const getGradeLabel = (grade) => {
    const labels = {
      1: '1+', 2: '1', 3: '2', 4: '3', 5: '4'
    };
    return labels[grade];
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f3f4f6' }}>
      {/* Header */}
      <div style={{
        background: '#1e40af',
        color: 'white',
        padding: '1rem',
        textAlign: 'center'
      }}>
        <h1 style={{ margin: 0, fontSize: '1.5rem' }}>🏀 Basketball Assessment</h1>
        <p style={{ margin: '0.5rem 0 0 0', opacity: 0.9 }}>
          Year 7 • 28 Students • 4 Groups
        </p>
      </div>

      {/* Group Selection */}
      {!currentGroup && (
        <div style={{
          padding: '2rem 1rem',
          display: 'grid',
          gridTemplateColumns: 'repeat(2, 1fr)',
          gap: '1rem'
        }}>
          {['A', 'B', 'C', 'D'].map(group => (
            <button
              key={group}
              onClick={() => loadGroup(group)}
              style={{
                padding: '2rem 1rem',
                backgroundColor: 'white',
                border: '2px solid #e5e7eb',
                borderRadius: '12px',
                fontSize: '1.2rem',
                fontWeight: 'bold',
                cursor: 'pointer',
                textAlign: 'center'
              }}
            >
              Group {group}<br />
              <small style={{ fontSize: '0.9rem', color: '#6b7280' }}>7 students</small>
            </button>
          ))}
        </div>
      )}

      {/* Students List */}
      {currentGroup && (
        <div>
          {/* Group Header */}
          <div style={{
            background: 'white',
            padding: '1rem',
            borderBottom: '1px solid #e5e7eb',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <div>
              <h2 style={{ margin: 0 }}>Group {currentGroup}</h2>
              <p style={{ margin: 0, color: '#6b7280' }}>{students.length} students</p>
            </div>
            <button
              onClick={() => setCurrentGroup(null)}
              style={{
                padding: '0.5rem 1rem',
                backgroundColor: '#f3f4f6',
                border: '1px solid #d1d5db',
                borderRadius: '6px',
                cursor: 'pointer'
              }}
            >
              Back to Groups
            </button>
          </div>

          {/* Students */}
          <div style={{ padding: '1rem' }}>
            {loading ? (
              <p style={{ textAlign: 'center' }}>Loading students...</p>
            ) : (
              students.map(student => (
                <div key={student.id} style={{
                  backgroundColor: 'white',
                  borderRadius: '12px',
                  padding: '1rem',
                  marginBottom: '1rem',
                  boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
                }}>
                  <h3 style={{ margin: '0 0 1rem 0' }}>{student.name}</h3>
                  
                  {/* Assessment Criteria */}
                  {['dribbling', 'passing', 'shooting', 'defense'].map(criterion => (
                    <div key={criterion} style={{ marginBottom: '1rem' }}>
                      <h4 style={{ 
                        margin: '0 0 0.5rem 0', 
                        fontSize: '1rem',
                        textTransform: 'capitalize'
                      }}>
                        {criterion}
                      </h4>
                      
                      {/* Grade Buttons */}
                      <div style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(5, 1fr)',
                        gap: '0.5rem'
                      }}>
                        {[1, 2, 3, 4, 5].map(grade => {
                          const isSelected = assessments[`${student.id}-${criterion}`] === grade;
                          return (
                            <button
                              key={grade}
                              onClick={() => createAssessment(student.id, criterion, grade)}
                              style={{
                                padding: '0.75rem 0.25rem',
                                border: '2px solid #e5e7eb',
                                borderRadius: '8px',
                                backgroundColor: isSelected ? getGradeColor(grade) : 'white',
                                color: isSelected ? 'white' : '#374151',
                                fontWeight: 'bold',
                                cursor: 'pointer',
                                fontSize: '0.9rem',
                                minHeight: '60px',
                                display: 'flex',
                                flexDirection: 'column',
                                alignItems: 'center',
                                justifyContent: 'center'
                              }}
                            >
                              <div>{getGradeLabel(grade)}</div>
                              <div style={{ fontSize: '0.7rem', opacity: 0.8 }}>
                                {grade === 1 ? 'Exc+' : grade === 2 ? 'Exc' : grade === 3 ? 'Met' : grade === 4 ? 'Below' : 'Low'}
                              </div>
                            </button>
                          );
                        })}
                      </div>
                    </div>
                  ))}
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;