import React from 'react';
import { SafeAreaView, ScrollView, StatusBar, StyleSheet, Text, View } from 'react-native';

export default function ScreenContainer({ title, description, children }) {
  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle="light-content" backgroundColor="#0A0E1A" />
      <View style={styles.topAccentLine} />
      <ScrollView contentContainerStyle={styles.container} showsVerticalScrollIndicator={false}>
        {(title || description) && (
          <View style={styles.header}>
            {!!title && <Text style={styles.title}>{title}</Text>}
            {!!description && <Text style={styles.description}>{description}</Text>}
          </View>
        )}
        <View style={styles.content}>{children}</View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#0A0E1A',
  },
  topAccentLine: {
    height: 2,
    backgroundColor: '#00D4FF',
    opacity: 0.9,
  },
  container: {
    padding: 20,
    paddingBottom: 28,
    gap: 18,
  },
  header: {
    gap: 8,
  },
  title: {
    fontSize: 28,
    fontWeight: '800',
    color: '#00D4FF',
    letterSpacing: 0.3,
  },
  description: {
    color: '#94A3B8',
    lineHeight: 21,
    fontSize: 14,
  },
  content: {
    gap: 14,
  },
});
