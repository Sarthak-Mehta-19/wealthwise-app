import { useEffect, useState } from 'react';
import { supabase } from './supabase.js'; // Imports the engine we made in Step 1

export function LiveChallenges() {
  const [challenges, setChallenges] = useState([]);

  useEffect(() => {
    // Subscribe to live changes
    const channel = supabase
      .channel('table-db-changes')
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'finance_app_challenge' },
        (payload) => {
          const { eventType, new: newRow, old: oldRow } = payload;
          setChallenges((prev) => {
            if (eventType === 'INSERT') return [newRow, ...prev];
            if (eventType === 'UPDATE') return prev.map(item => item.id === newRow.id ? newRow : item);
            if (eventType === 'DELETE') return prev.filter(item => item.id !== oldRow.id);
            return prev;
          });
        }
      )
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, []);

  return (
    <div>
      <h2>Live Group Challenges</h2>
      {challenges.map(challenge => (
        <div key={challenge.id}>
          <p>{challenge.title} - Target: ${challenge.target_amount}</p>
        </div>
      ))}
    </div>
  );
}