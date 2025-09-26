import { describe, expect, it } from '@jest/globals';
import {
  chmodSync,
  mkdtempSync,
  readFileSync,
  rmSync,
  statSync,
  writeFileSync
} from 'fs';
import * as os from 'os';
import { join } from 'path';

const loadManager = async () =>
  (await import('../auth/authentication-manager.js')).AuthenticationManager;

const BASE_URL = 'https://example.youtrack.cloud';

const createTempDir = (): { dir: string; restore: () => void } => {
  const tempDir = mkdtempSync(join(os.tmpdir(), 'auth-manager-test-'));

  return {
    dir: tempDir,
    restore: () => {
      rmSync(tempDir, { recursive: true, force: true });
    }
  };
};

describe('AuthenticationManager secure storage', () => {

  it('creates authentication file with owner-only permissions', async () => {
    const temp = createTempDir();

    try {
      const AuthenticationManager = await loadManager();
      const authFile = join(temp.dir, '.youtrack-mcp-auth.json');
      const manager = new AuthenticationManager({
        baseUrl: BASE_URL,
        token: 'secure-token',
        authStoragePath: authFile
      });
      await manager.getAuthToken();

      expect((manager as unknown as { authFile: string }).authFile).toBe(authFile);
      expect(() => statSync(authFile)).not.toThrow();
      const stats = statSync(authFile);

      expect(stats.mode & 0o777).toBe(0o600);

      const stored = JSON.parse(readFileSync(authFile, 'utf8'));
      expect(stored.data.token).toBe('secure-token');
    } finally {
      temp.restore();
    }
  });

  it('ignores cached credentials when permissions are too broad', async () => {
    const temp = createTempDir();

    try {
      const authFile = join(temp.dir, '.youtrack-mcp-auth.json');
      writeFileSync(
        authFile,
        JSON.stringify({
          type: 'token',
          baseUrl: BASE_URL,
          data: { token: 'cached-token' },
          lastUsed: Date.now()
        })
      );
      chmodSync(authFile, 0o644);

      const AuthenticationManager = await loadManager();
      const manager = new AuthenticationManager({
        baseUrl: BASE_URL,
        authStoragePath: authFile
      });
      expect((manager as unknown as { authFile: string }).authFile).toBe(authFile);
      const status = manager.getAuthStatus();

      expect(status.authenticated).toBe(false);
    } finally {
      temp.restore();
    }
  });

  it('loads cached credentials when permissions are secure', async () => {
    const temp = createTempDir();

    try {
      const authFile = join(temp.dir, '.youtrack-mcp-auth.json');
      writeFileSync(
        authFile,
        JSON.stringify({
          type: 'token',
          baseUrl: BASE_URL,
          data: { token: 'cached-token' },
          lastUsed: Date.now()
        })
      );
      chmodSync(authFile, 0o600);

      const AuthenticationManager = await loadManager();
      const manager = new AuthenticationManager({
        baseUrl: BASE_URL,
        authStoragePath: authFile
      });
      expect((manager as unknown as { authFile: string }).authFile).toBe(authFile);
      const status = manager.getAuthStatus();

      expect(status.authenticated).toBe(true);
      expect(status.type).toBe('token');
    } finally {
      temp.restore();
    }
  });
});

export {};
