import React from 'react';
import { SafeAreaView, ScrollView, StyleSheet, Text, View } from 'react-native';

export default function ScreenContainer({ title, description, children }) {
  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView contentContainerStyle={styles.container}>
        <View style={styles.header}>
          <Text style={styles.title}>{title}</Text>
          {!!description && <Text style={styles.description}>{description}</Text>}
        </View>
        <View style={styles.content}>{children}</View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#F5F7FA',
  },
  container: {
    padding: 20,
    gap: 16,
  },
  header: {
    gap: 8,
  },
  title: {
    fontSize: 26,
    fontWeight: '700',
    color: '#1D3557',
  },
  description: {
    color: '#457B9D',
    lineHeight: 20,
  },
  content: {
    gap: 12,
  },
});
