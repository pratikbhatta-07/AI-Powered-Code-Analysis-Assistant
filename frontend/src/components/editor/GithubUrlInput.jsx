import React, { useState } from 'react';
import { Github, Loader2 } from 'lucide-react';
import { fetchGithubCode } from '../../services/api';
import Button from '../common/Button';
import ErrorMessage from '../common/ErrorMessage';

const GithubUrlInput = ({ onCodeFetched }) => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFetch = async () => {
    if (!url.trim()) {
      setError('Please enter a GitHub URL');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetchGithubCode(url);
      onCodeFetched(response.code);
      setUrl('');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-3">
      <div className="flex gap-2">
        <div className="flex-1 relative">
          <Github className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleFetch()}
            placeholder="https://github.com/user/repo/blob/main/file.py"
            className="w-full bg-dark-surface border border-dark-border rounded-lg pl-10 pr-4 py-2.5 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-accent-primary/50 transition-colors"
          />
        </div>
        <Button
          onClick={handleFetch}
          disabled={loading || !url.trim()}
          className="flex items-center gap-2"
        >
          {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
          Fetch
        </Button>
      </div>
      {error && <ErrorMessage message={error} onDismiss={() => setError(null)} />}
    </div>
  );
};

export default GithubUrlInput;
