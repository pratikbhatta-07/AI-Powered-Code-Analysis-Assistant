export const ANALYSIS_MODES = [
  {
    id: '1',
    name: 'Beginner',
    label: 'Beginner Friendly',
    description: 'Step-by-step explanation for learning',
    icon: 'GraduationCap',
    color: 'text-green-400',
  },
  {
    id: '2',
    name: 'Interview',
    label: 'Interview Style',
    description: 'Technical analysis for interview prep',
    icon: 'Briefcase',
    color: 'text-blue-400',
  },
  {
    id: '3',
    name: 'Tests',
    label: 'Test Generation',
    description: 'Generate comprehensive test cases',
    icon: 'TestTube',
    color: 'text-purple-400',
  },
  {
    id: '4',
    name: 'Bugs',
    label: 'Find Bugs',
    description: 'Identify potential issues and risks',
    icon: 'Bug',
    color: 'text-red-400',
  },
  {
    id: '5',
    name: 'Full',
    label: 'Full Review',
    description: 'Complete analysis: explanation + complexity + tests + bugs',
    icon: 'Layers',
    color: 'text-cyan-400',
  },
];

export const LANGUAGES = [
  { id: 'python', name: 'Python', extension: '.py' },
  { id: 'javascript', name: 'JavaScript', extension: '.js' },
  { id: 'java', name: 'Java', extension: '.java' },
  { id: 'cpp', name: 'C++', extension: '.cpp' },
  { id: 'c', name: 'C', extension: '.c' },
  { id: 'typescript', name: 'TypeScript', extension: '.ts' },
  { id: 'go', name: 'Go', extension: '.go' },
  { id: 'rust', name: 'Rust', extension: '.rs' },
];

export const INPUT_METHODS = {
  PASTE: 'paste',
  FILE: 'file',
  GITHUB: 'github',
};
