import React from 'react';
import ThreadCard from './ThreadCard';

/**
 * ThreadsList Component
 * Renders a list of threads with scrollable container
 *
 * @param {Object} props
 * @param {Array} props.threads - Array of thread objects
 */
const ThreadsList = ({ threads }) => {
  return (
    <div className="flex flex-col gap-4 overflow-y-auto h-full pr-2">
      {threads.map((thread) => (
        <ThreadCard key={thread.id} thread={thread} />
      ))}
    </div>
  );
};

export default ThreadsList;
