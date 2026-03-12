import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

import ScreenContainer from '../../components/ScreenContainer';

export default function HomeScreen() {
  return (
    <ScreenContainer
      title="Accueil"
      description="Tableau de bord Check-IA: résumé des vérifications récentes et signaux de risque."
    >
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Analyses aujourd'hui</Text>
        <Text style={styles.cardValue}>12</Text>
      </View>
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Alertes deepfake</Text>
        <Text style={styles.cardValue}>3 médias suspects</Text>
      </View>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 16,
  },
  cardTitle: {
    color: '#457B9D',
    marginBottom: 8,
  },
  cardValue: {
    color: '#1D3557',
    fontSize: 22,
    fontWeight: '700',
  },
});
