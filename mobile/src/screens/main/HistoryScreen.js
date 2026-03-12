import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

import ScreenContainer from '../../components/ScreenContainer';

const MOCK_HISTORY = [
  { title: 'Discours politique viral', verdict: 'mixed' },
  { title: 'Vidéo manipulation locale', verdict: 'false' },
];

export default function HistoryScreen() {
  return (
    <ScreenContainer title="Historique" description="Retrouvez les dernières analyses effectuées.">
      {MOCK_HISTORY.map((item) => (
        <View key={item.title} style={styles.row}>
          <Text style={styles.title}>{item.title}</Text>
          <Text style={styles.verdict}>{item.verdict.toUpperCase()}</Text>
        </View>
      ))}
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  row: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 14,
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  title: {
    color: '#1D3557',
    fontWeight: '600',
  },
  verdict: {
    color: '#E63946',
    fontWeight: '700',
  },
});
