import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

import ScreenContainer from '../../components/ScreenContainer';

const MOCK_HISTORY = [
  { title: 'Discours politique viral sur la sécurité régionale', score: 35, source: 'Réseaux sociaux', date: '2026-02-12' },
  { title: 'Vidéo manipulation locale partagée dans un groupe', score: 78, source: 'Signal citoyen', date: '2026-02-09' },
  { title: 'Annonce économique attribuée à tort à un ministre', score: 55, source: 'Blog', date: '2026-02-02' },
];

const getColor = (score) => {
  if (score >= 70) return '#10B981';
  if (score < 40) return '#EF4444';
  return '#F59E0B';
};

export default function HistoryScreen() {
  return (
    <ScreenContainer title="Historique" description="Retrouvez les dernières analyses effectuées.">
      {MOCK_HISTORY.map((item) => (
        <View key={item.title} style={styles.row}>
          <Text style={styles.title} numberOfLines={1}>
            {item.title}
          </Text>
          <View style={styles.bottomRow}>
            <Text style={styles.meta}>{item.source}</Text>
            <Text style={styles.meta}>{new Date(item.date).toLocaleDateString()}</Text>
          </View>
          <View style={[styles.badge, { borderColor: getColor(item.score) }]}>
            <Text style={[styles.badgeText, { color: getColor(item.score) }]}>{item.score}%</Text>
          </View>
        </View>
      ))}
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  row: {
    backgroundColor: '#111827',
    borderRadius: 12,
    padding: 14,
    borderWidth: 1,
    borderColor: '#1E293B',
    gap: 8,
  },
  title: {
    color: '#FFFFFF',
    fontWeight: '700',
  },
  bottomRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  meta: {
    color: '#94A3B8',
    fontSize: 12,
  },
  badge: {
    alignSelf: 'flex-start',
    borderWidth: 1,
    borderRadius: 999,
    paddingHorizontal: 10,
    paddingVertical: 3,
  },
  badgeText: {
    fontWeight: '800',
    fontSize: 12,
  },
});
