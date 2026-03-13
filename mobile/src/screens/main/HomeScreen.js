import React, { useEffect, useMemo, useState } from 'react';
import { ActivityIndicator, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { useNavigation } from '@react-navigation/native';

import ScreenContainer from '../../components/ScreenContainer';
import api from '../../services/api';

const getScore = (item) => {
  if (typeof item?.score === 'number') {
    return item.score;
  }
  if (typeof item?.confidence_score === 'number') {
    return item.confidence_score;
  }
  if (typeof item?.veracity_score === 'number') {
    return item.veracity_score;
  }
  return 50;
};

export default function HomeScreen() {
  const navigation = useNavigation();
  const [trending, setTrending] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchTrending = async () => {
      setLoading(true);
      try {
        const response = await api.get('/facts/trending/');
        setTrending(response.data || []);
      } catch (error) {
        setTrending([]);
      } finally {
        setLoading(false);
      }
    };

    fetchTrending();
  }, []);

  const stats = useMemo(() => {
    const total = trending.length;
    const fake = trending.filter((item) => getScore(item) < 40).length;
    const verified = trending.filter((item) => getScore(item) >= 70).length;
    return { total, fake, verified };
  }, [trending]);

  return (
    <ScreenContainer title="Bonjour 👋" description="Tableau de bord">
      <View style={styles.statsRow}>
        <View style={styles.statCard}>
          <Text style={styles.statValue}>{stats.total}</Text>
          <Text style={styles.statLabel}>Total vérifications</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={[styles.statValue, { color: '#EF4444' }]}>{stats.fake}</Text>
          <Text style={styles.statLabel}>Faux détectés</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={[styles.statValue, { color: '#10B981' }]}>{stats.verified}</Text>
          <Text style={styles.statLabel}>Vrais confirmés</Text>
        </View>
      </View>

      <TouchableOpacity style={styles.ctaButton} onPress={() => navigation.navigate('Scan')}>
        <Text style={styles.ctaText}>Analyser maintenant</Text>
      </TouchableOpacity>

      <View style={styles.sectionCard}>
        <Text style={styles.sectionTitle}>Vérifications tendances</Text>
        {loading ? (
          <ActivityIndicator color="#00D4FF" />
        ) : trending.length === 0 ? (
          <View style={styles.emptyState}>
            <Text style={styles.emptyIcon}>🛡️</Text>
            <Text style={styles.emptyText}>Aucune vérification publique disponible.</Text>
          </View>
        ) : (
          trending.slice(0, 8).map((item) => {
            const score = Math.max(0, Math.min(100, Number(getScore(item))));
            const barColor = score >= 70 ? '#10B981' : '#EF4444';
            return (
              <View key={String(item.id)} style={styles.factCard}>
                <Text style={styles.factTitle} numberOfLines={2}>
                  {item.title || 'Vérification sans titre'}
                </Text>
                <View style={styles.metaRow}>
                  <Text style={styles.sourceBadge}>{item.source || 'Source inconnue'}</Text>
                  <Text style={styles.dateText}>{new Date(item.created_at || Date.now()).toLocaleDateString()}</Text>
                </View>
                <View style={styles.scoreTrack}>
                  <View style={[styles.scoreFill, { width: `${score}%`, backgroundColor: barColor }]} />
                </View>
                <Text style={[styles.scoreText, { color: barColor }]}>Score: {score}%</Text>
              </View>
            );
          })
        )}
      </View>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  statsRow: {
    flexDirection: 'row',
    gap: 10,
  },
  statCard: {
    flex: 1,
    backgroundColor: '#111827',
    borderRadius: 14,
    padding: 12,
    borderWidth: 1,
    borderColor: '#1E293B',
  },
  statValue: {
    color: '#00D4FF',
    fontSize: 22,
    fontWeight: '800',
  },
  statLabel: {
    color: '#94A3B8',
    fontSize: 12,
    marginTop: 4,
  },
  ctaButton: {
    backgroundColor: '#00D4FF',
    borderRadius: 14,
    paddingVertical: 14,
    alignItems: 'center',
  },
  ctaText: {
    color: '#0A0E1A',
    fontWeight: '800',
    fontSize: 15,
  },
  sectionCard: {
    backgroundColor: '#111827',
    borderRadius: 16,
    padding: 14,
    borderWidth: 1,
    borderColor: '#1E293B',
  },
  sectionTitle: {
    color: '#FFFFFF',
    marginBottom: 10,
    fontWeight: '700',
    fontSize: 16,
  },
  factCard: {
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#1E293B',
    backgroundColor: '#0F172A',
    padding: 12,
    marginBottom: 10,
  },
  factTitle: {
    color: '#FFFFFF',
    fontWeight: '600',
    marginBottom: 8,
  },
  metaRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  sourceBadge: {
    color: '#00D4FF',
    borderWidth: 1,
    borderColor: '#00D4FF',
    borderRadius: 20,
    paddingHorizontal: 10,
    paddingVertical: 3,
    fontSize: 11,
    overflow: 'hidden',
  },
  dateText: {
    color: '#94A3B8',
    fontSize: 11,
  },
  scoreTrack: {
    height: 8,
    borderRadius: 999,
    backgroundColor: '#1E293B',
    overflow: 'hidden',
  },
  scoreFill: {
    height: '100%',
    borderRadius: 999,
  },
  scoreText: {
    marginTop: 6,
    fontWeight: '700',
    fontSize: 12,
  },
  emptyState: {
    alignItems: 'center',
    paddingVertical: 20,
  },
  emptyIcon: {
    fontSize: 30,
    marginBottom: 8,
  },
  emptyText: {
    color: '#94A3B8',
    textAlign: 'center',
  },
});
