import React from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';

import ScreenContainer from '../../components/ScreenContainer';

export default function ProfileScreen({ navigation }) {
  const username = 'Utilisateur Demo';
  const email = 'demo@check-ia.app';
  const initials = username
    .split(' ')
    .map((chunk) => chunk[0])
    .join('')
    .slice(0, 2)
    .toUpperCase();

  return (
    <ScreenContainer title="Profil" description="Gestion du compte et préférences de vérification.">
      <View style={styles.profileCard}>
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>{initials}</Text>
        </View>
        <Text style={styles.name}>{username}</Text>
        <Text style={styles.email}>{email}</Text>
      </View>

      <View style={styles.statsRow}>
        <View style={styles.statCard}>
          <Text style={styles.statValue}>42</Text>
          <Text style={styles.statLabel}>Analyses</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={[styles.statValue, { color: '#10B981' }]}>18</Text>
          <Text style={styles.statLabel}>Fiables</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={[styles.statValue, { color: '#EF4444' }]}>9</Text>
          <Text style={styles.statLabel}>Alertes</Text>
        </View>
      </View>

      <Pressable style={styles.logoutButton} onPress={() => navigation.replace('Auth')}>
        <Text style={styles.logoutText}>Se déconnecter</Text>
      </Pressable>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  profileCard: {
    backgroundColor: '#111827',
    borderRadius: 16,
    padding: 20,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#1E293B',
  },
  avatar: {
    width: 76,
    height: 76,
    borderRadius: 38,
    backgroundColor: '#0F172A',
    borderWidth: 2,
    borderColor: '#00D4FF',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 12,
  },
  avatarText: {
    color: '#00D4FF',
    fontSize: 26,
    fontWeight: '900',
  },
  name: {
    fontSize: 20,
    color: '#FFFFFF',
    fontWeight: '700',
  },
  email: {
    color: '#94A3B8',
    marginTop: 5,
  },
  statsRow: {
    flexDirection: 'row',
    gap: 10,
  },
  statCard: {
    flex: 1,
    backgroundColor: '#111827',
    borderRadius: 14,
    borderWidth: 1,
    borderColor: '#1E293B',
    padding: 12,
  },
  statValue: {
    color: '#00D4FF',
    fontSize: 20,
    fontWeight: '800',
  },
  statLabel: {
    marginTop: 3,
    color: '#94A3B8',
    fontSize: 12,
  },
  logoutButton: {
    borderWidth: 1,
    borderColor: '#EF4444',
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: 'center',
    backgroundColor: '#111827',
  },
  logoutText: {
    color: '#EF4444',
    fontWeight: '700',
  },
});
