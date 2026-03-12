import React, { useEffect, useState } from 'react';
import { ActivityIndicator, FlatList, StyleSheet, Text, View } from 'react-native';

import ScreenContainer from '../../components/ScreenContainer';
import api from '../../services/api';

export default function HomeScreen() {
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

  return (
    <ScreenContainer
      title="Accueil"
      description="Tableau de bord Check-IA: résumé des vérifications récentes et signaux de risque."
    >
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Vérifications tendances</Text>
        {loading ? (
          <ActivityIndicator color="#1D3557" />
        ) : (
          <FlatList
            data={trending}
            keyExtractor={(item) => String(item.id)}
            ListEmptyComponent={<Text style={styles.empty}>Aucune vérification publique disponible.</Text>}
            renderItem={({ item }) => (
              <View style={styles.factRow}>
                <Text style={styles.factTitle}>{item.title}</Text>
                <Text style={styles.factMeta}>{String(item.verdict || 'unknown').toUpperCase()}</Text>
              </View>
            )}
          />
        )}
      </View>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 16,
    minHeight: 220,
  },
  cardTitle: {
    color: '#457B9D',
    marginBottom: 12,
    fontWeight: '700',
  },
  factRow: {
    borderBottomWidth: 1,
    borderBottomColor: '#E9EEF4',
    paddingVertical: 10,
  },
  factTitle: {
    color: '#1D3557',
    fontWeight: '600',
  },
  factMeta: {
    color: '#6B7C93',
    fontSize: 12,
    marginTop: 2,
  },
  empty: {
    color: '#6B7C93',
  },
});
