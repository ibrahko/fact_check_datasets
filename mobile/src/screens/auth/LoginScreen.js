import React, { useState, useCallback } from 'react';
import {
  ActivityIndicator,
  Alert,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from 'react-native';
import api, { saveTokens } from '../../services/api';

export default function LoginScreen({ navigation, route }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [focusedField, setFocusedField] = useState(null);

  const successMessage = route?.params?.successMessage;

  const getErrorMessage = (err) => {
    const data = err?.response?.data;
    if (!data) return 'Impossible de se connecter. Vérifiez votre connexion.';
    if (typeof data === 'string' && data.includes('<!DOCTYPE')) return 'Erreur serveur. Veuillez réessayer.';
    if (data?.detail) return data.detail;
    if (data?.non_field_errors) return data.non_field_errors[0];
    return 'Identifiants incorrects. Veuillez réessayer.';
  };

  const handleLogin = useCallback(async () => {
    if (loading) return;
    if (!username.trim() || !password.trim()) {
      setError('Veuillez remplir tous les champs.');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const response = await api.post('/auth/login/', { username: username.trim(), password });
      // Backend retourne { user: {...}, tokens: { access, refresh } }
      const tokens = response.data.tokens || response.data;
      await saveTokens(tokens);
      navigation.replace('Main');
    } catch (err) {
      const message = getErrorMessage(err);
      setError(message);
    } finally {
      setLoading(false);
    }
  }, [username, password, loading]);

  return (
    <KeyboardAvoidingView
      style={styles.screen}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        keyboardShouldPersistTaps="handled"
        showsVerticalScrollIndicator={false}
      >
        {/* HEADER */}
        <View style={styles.header}>
          <Text style={styles.logoIcon}>🛡️</Text>
          <Text style={styles.logoText}>CHECK-IA</Text>
          <Text style={styles.subtitle}>Vérifiez. Analysez. Protégez.</Text>
          <Text style={styles.tagline}>Combattre la désinformation{"\n"}avec l'intelligence artificielle</Text>
        </View>

        {/* CARD */}
        <View style={styles.card}>
          {/* SUCCESS / ERROR */}
          {successMessage ? (
            <View style={styles.successBanner}>
              <Text style={styles.successText}>✅ {successMessage}</Text>
            </View>
          ) : null}
          {error ? (
            <View style={styles.errorBanner}>
              <Text style={styles.errorText}>⚠️ {error}</Text>
            </View>
          ) : null}

          {/* USERNAME */}
          <Text style={styles.label}>Nom d'utilisateur</Text>
          <TextInput
            style={[styles.input, focusedField === 'username' && styles.inputFocused]}
            placeholder="Votre nom d'utilisateur"
            placeholderTextColor="#475569"
            value={username}
            onChangeText={setUsername}
            autoCapitalize="none"
            autoCorrect={false}
            returnKeyType="next"
            onFocus={() => setFocusedField('username')}
            onBlur={() => setFocusedField(null)}
          />

          {/* PASSWORD */}
          <Text style={styles.label}>Mot de passe</Text>
          <View style={styles.passwordContainer}>
            <TextInput
              style={[styles.input, styles.passwordInput, focusedField === 'password' && styles.inputFocused]}
              placeholder="Votre mot de passe"
              placeholderTextColor="#475569"
              value={password}
              onChangeText={setPassword}
              secureTextEntry={!showPassword}
              returnKeyType="done"
              onSubmitEditing={handleLogin}
              onFocus={() => setFocusedField('password')}
              onBlur={() => setFocusedField(null)}
            />
            <TouchableOpacity
              style={styles.eyeButton}
              onPress={() => setShowPassword(v => !v)}
              hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
            >
              <Text style={styles.eyeIcon}>{showPassword ? '🙈' : '👁️'}</Text>
            </TouchableOpacity>
          </View>

          {/* LOGIN BUTTON */}
          <TouchableOpacity
            style={[styles.primaryButton, loading && styles.buttonDisabled]}
            onPress={handleLogin}
            disabled={loading}
            activeOpacity={0.8}
          >
            {loading ? (
              <ActivityIndicator color="#0A0E1A" size="small" />
            ) : (
              <Text style={styles.primaryButtonText}>Se connecter</Text>
            )}
          </TouchableOpacity>

          {/* REGISTER LINK */}
          <TouchableOpacity
            style={styles.secondaryButton}
            onPress={() => navigation.navigate('Register')}
            disabled={loading}
            activeOpacity={0.8}
          >
            <Text style={styles.secondaryButtonText}>Créer un compte</Text>
          </TouchableOpacity>
        </View>

        <Text style={styles.footer}>AgentsIA © 2026 — Check-IA v1.0</Text>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: '#0A0E1A' },
  scrollContent: {
    flexGrow: 1,
    paddingHorizontal: 24,
    paddingTop: 60,
    paddingBottom: 40,
  },
  header: { alignItems: 'center', marginBottom: 32 },
  logoIcon: { fontSize: 56, marginBottom: 8 },
  logoText: {
    fontSize: 38,
    fontWeight: '900',
    color: '#00D4FF',
    letterSpacing: 2,
  },
  subtitle: {
    fontSize: 15,
    color: '#FFFFFF',
    fontWeight: '700',
    marginTop: 6,
  },
  tagline: {
    marginTop: 8,
    textAlign: 'center',
    color: '#94A3B8',
    fontSize: 13,
    lineHeight: 20,
  },
  card: {
    backgroundColor: '#111827',
    borderRadius: 20,
    padding: 20,
    borderWidth: 1,
    borderColor: '#1E293B',
  },
  successBanner: {
    backgroundColor: '#064E3B',
    borderRadius: 10,
    padding: 10,
    marginBottom: 12,
  },
  successText: { color: '#10B981', fontSize: 13 },
  errorBanner: {
    backgroundColor: '#450A0A',
    borderRadius: 10,
    padding: 10,
    marginBottom: 12,
  },
  errorText: { color: '#FCA5A5', fontSize: 13 },
  label: {
    color: '#FFFFFF',
    fontWeight: '700',
    fontSize: 14,
    marginBottom: 6,
    marginTop: 12,
  },
  input: {
    borderWidth: 1.5,
    borderColor: '#1E293B',
    borderRadius: 12,
    paddingHorizontal: 14,
    paddingVertical: 14,
    backgroundColor: '#0F172A',
    color: '#FFFFFF',
    fontSize: 15,
  },
  inputFocused: { borderColor: '#00D4FF' },
  passwordContainer: { position: 'relative' },
  passwordInput: { paddingRight: 50 },
  eyeButton: {
    position: 'absolute',
    right: 14,
    top: 0,
    bottom: 0,
    justifyContent: 'center',
  },
  eyeIcon: { fontSize: 20 },
  primaryButton: {
    marginTop: 20,
    backgroundColor: '#00D4FF',
    borderRadius: 14,
    paddingVertical: 16,
    alignItems: 'center',
  },
  buttonDisabled: { opacity: 0.6 },
  primaryButtonText: {
    color: '#0A0E1A',
    fontSize: 16,
    fontWeight: '800',
    letterSpacing: 0.5,
  },
  secondaryButton: {
    marginTop: 12,
    borderRadius: 14,
    borderWidth: 1.5,
    borderColor: '#00D4FF',
    paddingVertical: 14,
    alignItems: 'center',
  },
  secondaryButtonText: {
    color: '#00D4FF',
    fontWeight: '700',
    fontSize: 15,
  },
  footer: {
    textAlign: 'center',
    color: '#334155',
    fontSize: 11,
    marginTop: 24,
  },
});
